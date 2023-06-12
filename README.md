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

## TODO

#### Support

- [ ] render dashboard
- [X] frontend route switch without taking over the page
- [X] ability to send emails to login
- [X] spooler
- [X] user_ids should be UUIDs
- [ ] style pages

#### Allow users to add words to their list

- [ ] management command to add vocabulary from CEDICT.txt
- [ ] search endpoint that allows for hanzi or pinyin
- [ ] endpoint to add words to user list

#### Quiz page

- [ ] render quiz page
- [ ] frontend component display question
- [ ] endpoint to submit answer

Types of questions for words: accents from Hanzi, definitions from Hanzi, hanzi from English

#### Allow users to add grammar rules

- [ ] management command to add grammar rules from txt file or via command line
- [ ] allow users to search for grammar rules by component words
- [ ] allow users to CRUD their own grammar rules (combination of words and parts of speech)
- [ ] async job that populates grammar rule examples from ChatGPT
- [ ] add grammar rules to quiz page

#### Add Stripe Payments

- [ ] redirect to Stripe payment dashboard

#### Deployment

- [ ] create production Dockerfile
- [ ] create production uwsgi config
- [ ] app platform

## Progress

#### 06/10/2023

- [X] frontend route switch without taking over the page
- [X] user_ids should be UUIDs
- [X] spooler
- [X] ability to send emails to login and verify

#### Next Day

- [X] management command to add vocabulary from CEDICT.txt
- [ ] search endpoint that allows for hanzi or pinyin
- [ ] add search bar to dashboard
