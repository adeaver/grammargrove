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

Any management commands can be run with:

```
./scripts/manage {command}
```

This is merely a convenience around `docker exec -it grammargrove-web-1 poetry run ./manage.py {command}`, which needs to be used to interact with the database.

## TODO

#### Support

- [ ] render dashboard
- [ ] frontend route switch without taking over the page
- [ ] spooler
- [ ] ability to send emails to login
- [ ] user_ids should be UUIDs
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
