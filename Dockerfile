FROM alpine:3.17.3 as frontend-builder

# npm
RUN apk update && apk add npm

WORKDIR /app

# Install dependencies
COPY frontend/package.json .
COPY frontend/package-lock.json .

RUN npm install --omit=dev

COPY frontend/src ./src
COPY frontend/postcss.config.js .
COPY frontend/tailwind.config.js .
COPY frontend/tsconfig.json .
COPY frontend/tsconfig.node.json .
COPY frontend/vite.config.development.ts .
COPY frontend/vite.config.ts .
COPY frontend/index.html .

RUN npm run build

FROM python:3.10.12-bullseye

WORKDIR /app

ENV SERVICE_USER somebody
RUN groupadd $SERVICE_USER && useradd -m -g $SERVICE_USER -l $SERVICE_USER

RUN apt-get update -y && apt-get install -y postgresql
RUN pip3 install poetry

COPY pyproject.toml .
COPY poetry.lock . 
RUN poetry install -vvv

COPY . .
RUN rm -rf ./frontend
COPY --from=frontend-builder /app/dist/assets/index.js /app/index.js
COPY --from=frontend-builder /app/dist/assets/index.css /app/index.css

RUN mkdir -p /var/log/uwsgi
RUN mkdir -p /var/uwsgi

RUN poetry run ./manage.py collectstatic --noinput

CMD [ "scripts/runserver" ]
