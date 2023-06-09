# GrammarGrove

#### Getting started

Currently using Python version 3.10.12, this can be installed using [pyenv](https://github.com/pyenv/pyenv)

You're also going to need to install Django for use of the command line tools.

#### Running the server

```
docker-compose up --build
```

And head over to http://localhost:8000/

#### Running commands

Any management commands that need to be run against the database can be run with:

```
docker exec -it grammargrove-web-1 poetry run ./manage.py {command}
```

Any management commands that don't need database access (makemigrations included) can also be run with that or simply:

```
poetry run ./manage.py {command}
```

## TODO

- [X] Getting postgres database working
- [X] Run webserver with uWSGI
- [X] User model
