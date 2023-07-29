# GrammarGrove

#### Getting started

Currently using Python version 3.10.12, this can be installed using [pyenv](https://github.com/pyenv/pyenv)

You're also going to need to install Django for use of the command line tools.

#### Download the dictionary

We currently use the [CEDICT](https://www.mdbg.net/chinese/dictionary?page=cedict) for a basic dictionary. You will want to download it, unzip it, and move it words/data/cedict.txt

#### Running the server

```
docker-compose up --build
```

And head over to http://localhost:8000/

#### Running commands

Any management commands can be run with:

```
./scripts/manage {command}
```

This is merely a convenience around `docker exec -it grammargrove-web-1 poetry run ./manage.py {command}`, which needs to be used to interact with the database.

## Code Layout

All frontend files live in the conveniently named `frontend/` directory. We use Preact for the frontend, but it's effectively the same thing as React.

We use Django for the backend. With the exception of `scripts/` and `conf/`, all the remaining directories are django apps.
- `scripts/` is for various scripts that improve our lives
- `conf/` is for our nginx configuration
- `cron.d/` is any crontab scripts that need to get run on the server. For Python cron jobs, use `grammargrove/tasks.py` instead

Some special cases to be aware of:
- `grammargrove/` is the main project directory. Things related to uWSGI also live in here.
- `index/` is for serving the frontend. React-Router is kind of garbage and makes authentication harder than it needs to be, so we serve everything from the backend.

## Deploying

We run on DigitalOcean. If we need to create a new Droplet, add the tag `grammargrove-web` to it so that the firewall rules apply to it.

On the Droplet, [install the official Docker Engine](https://docs.docker.com/engine/install/ubuntu/)

Make the following directories:
```
mkdir -p $REPO_HOME/grammargrove/log $REPO_HOME/grammargrove/uwsgi $REPO_HOME/grammargrove/webroot/dhparam
```

Run the following command:
```
sudo openssl dhparam -out $REPO_HOME/grammargrove/webroot/dhparam/dhparam-2048.pem 2048
```

To start the deployment:
```
docker compose -f prod-compose.yaml up --build
```

A note here: nginx may fail to load because of SSL, comment those lines out of `conf/nginx.conf`

You can deploy the server with:
```
./scripts/deploy-web
```
