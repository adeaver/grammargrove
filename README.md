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

Some special cases to be aware of:
- `grammargrove/` is the main project directory. Things related to uWSGI also live in here.
- `index/` is for serving the frontend. React-Router is kind of garbage and makes authentication harder than it needs to be, so we serve everything from the backend.
