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

We use Django for the backend. With the exception of `scripts/`, all the remaining directories are django apps.

Some special cases to be aware of:
- `grammargrove/` is the main project directory. Things related to uWSGI also live in here.
- `index/` is for serving the frontend. React-Router is kind of garbage and makes authentication harder than it needs to be, so we serve everything from the backend.


## Outstanding TODO for MVP

#### Support
- [X] style index page
- [ ] add "already have an account?" to index page
- [ ] redo dashboard to include both user vocabulary and word search
- [ ] style quiz page
- [ ] restyle "How it works" section with styled components from quiz and dashboard pages
- [ ] management command to apply hsk labels to grammar rules and words
- [ ] populate grammarrules.csv

#### Allow users to add words to their list
- [X] Page to display vocabulary and search within vocabulary
- [ ] Add notes to user vocabulary (not super necessary, can be a fast follow)

#### Quiz page
- [ ] handle case in which a user has nothing to quiz
- [X] add grammar rules to quiz page

#### Bugs to fix
- [X] Pinyin search should allow for both numbered and actual pinyin
- [x] Frontend should display accents not as numbers
- [ ] Enter should work on forms
- [ ] Infra: frontend doesn't always rerender (fast follow)
- [ ] Word search results should include user vocabulary ID
- [ ] refresh page on user vocabulary

#### Tech Debt
- [X] Clean up search endpoint for grammar rules using nested serializers
- [ ] See if you can clean up grammar rule examples

#### Add Stripe Payments
- [ ] redirect to Stripe payment dashboard
- [ ] webhook for continuing payments
- [ ] spooler job to check expiring payments

#### Deployment
- [ ] create production Dockerfile for web and postgres
- [ ] create production uwsgi config
- [ ] remove all migrations and re-run makemigrations
- [ ] write scripts to setup ufw on servers
- [ ] write nginx configuration and use certbot (steal from Babblegraph)

#### Wishlist
- [ ] Search without accents (fast follow)

## Progress 06/18/2023-06/24/2023

#### Next Day
- [ ] add style to user grammar rules
- [ ] add link to quiz page
- [ ] add "already have an account?" to index page

#### 06/21/2023
- [X] Style index page
- [X] Add style to user vocabulary words

#### 06/20/2023
- [X] Clean up search endpoint for grammar rules using nested serializers
- [X] Use django choices for LanguageCode
- [X] Page to display vocabulary and search within vocabulary
- [X] Pinyin search should allow for both numbered and actual pinyin
- [x] Frontend should display accents not as numbers

#### 06/19/2023
- [X] add grammar rules to quiz page
- [X] Page to display vocabulary and search within vocabulary

## Done for MVP

#### Support
- [X] render dashboard
- [X] frontend route switch without taking over the page
- [X] ability to send emails to login
- [X] spooler
- [X] user_ids should be UUIDs
- [X] spooler cron

#### Allow users to add words to their list
- [X] management command to add vocabulary from CEDICT.txt
- [X] search endpoint that allows for hanzi or pinyin
- [X] endpoint to add words to user list

#### Quiz page
- [X] render quiz page
- [X] frontend component display question
- [X] endpoint to submit answer

Types of questions for words: accents from Hanzi, definitions from Hanzi, hanzi from English

#### Allow users to add grammar rules
- [X] management command to add grammar rules from txt file or via command line
- [X] allow users to search for grammar rules by component words
- [X] allow users to CRUD their own grammar rules (combination of words and parts of speech)
- [X] Functions to get grammar rule examples from ChatGPT
- [X] Function to parse response from ChatGPT and save models
- [X] async job that populates grammar rule examples
- [X] script to load in grammar rules should take in human verified examples to prompt ChatGPT

-> Example prompt for (subject+是+predicate+的):

In Mandarin, the sentence structure "subject+是+在+place+verb+的" is used for emphasizing where something is done. For example, "我 是 在 香港 出生 的 " emphasizes that the birth happened in Hong Kong. In this example, 我 is the subject, 香港 is the place, 出生 is the verb.
Please write a CSV file with 10 example sentences using this sentence structure and only vocabulary from HSK1 and HSK2? The headers should be "Simplified characters,pinyin,English Definition".

-> Prompt format

In Mandarin, the sentence structure {structure} is used for {use}. For example, {example} {explanation}. In this example, {word} is {function}.
Please write a CSV file with 10 example sentences using this sentence structure and only vocabulary from HSK1 and HSK2? The headers should be "Simplified characters,pinyin,English Definition".

-> Create CSV:

grammar_rule_line_number,structure,use,hanzi,pinyin,explanation
1,subject 是 在 place verb 的,emphasizing where something is done,我 是 在 香港 出生 的,Wǒ shì zài Xiānggǎng chūshēng de,emphasizes that the birth happened in Hong Kong

#### Bugs to fix
- [ ] Pinyin search should allow for both numbered and actual pinyin
- [X] Dashboard should require auth, as well as search page
- [ ] Frontend should display accents not as numbers
- [ ] Enter should work on forms
- [ ] Infra: frontend doesn't always rerender
- [ ] Definitions for phrases should be stripped of punctuation, trimmed, and lowercased on quizzes

#### Tech Debt
- [X] Word search bar should be a separate component
- [X] Clean up search endpoint for grammar rules using nested serializers
- [ ] See if you can clean up grammar rule examples

#### Add Stripe Payments
- [ ] redirect to Stripe payment dashboard
- [ ] webhook for continuing payments
- [ ] spooler job to check expiring payments

#### Deployment
- [ ] create production Dockerfile
- [ ] create production uwsgi config
- [ ] figure out deployment strategy (managed db is probably not going to work because of space limit)

#### Wishlist
- [ ] Search without accents

## Progress 06/10/2023-06/17/2023

#### 06/10/2023
- [X] frontend route switch without taking over the page
- [X] user_ids should be UUIDs
- [X] spooler
- [X] ability to send emails to login and verify

#### 06/12/2023
- [X] management command to add vocabulary from CEDICT.txt
- [X] add search bar to dashboard
- [X] search endpoint that allows for hanzi or pinyin
- [X] Render cards for displaying words
- [X] Endpoint to allow users to CRUD words to their vocabulary

#### 06/13/2023
- [X] render quiz page
- [X] frontend component display question
- [X] endpoint to submit answer

#### 06/14/2023
- [X] management command to add grammar rules from txt file or via command line
- [X] allow users to search for grammar rules by component words

#### 06/15/2023
- [X] Frontend to search for grammar rules
- [X] allow users to CRUD their own grammar rules (combination of words and parts of speech)
- [X] spooler cron

#### 06/17/2023
- [X] Functions to get grammar rule examples from ChatGPT
- [X] Function to parse response from ChatGPT and save models
- [X] async job that populates grammar rule examples
- [X] script to load in grammar rules should take in human verified examples to prompt ChatGPT
