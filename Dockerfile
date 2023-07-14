FROM alpine:3.17.3 as frontend-builder

# npm
RUN apk update && apk add npm

WORKDIR /app

# Install dependencies
COPY frontend/package.json .
COPY frontend/package-lock.json .

RUN npm install

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
RUN pip3 install uwsgi

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install

COPY . .
RUN rm ./index/static/*
RUN rm -rf ./frontend
COPY --from=frontend-builder /app/dist/assets/index.js ./index/static/index.js
COPY --from=frontend-builder /app/dist/assets/index.css ./index/static/index.css

RUN poetry run ./manage.py collectstatic --noinput

USER $SERVICE_USER

CMD [ "scripts/runserver" ]
