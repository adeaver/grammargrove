# Outstanding TODO for MVP

#### Support
- [X] style index page
- [ ] add "already have an account?" to index page
- [X] redo dashboard to include both user vocabulary and word search
- [X] style quiz page
- [X] restyle "How it works" section with styled components from quiz and dashboard pages
- [X] management command to apply hsk labels to grammar rules and words
- [X] populate grammarrules.csv
- [X] Add pagination button to user grammar rules display view
- [X] Add pagination buttons to grammar rules search result view
- [ ] How to search page
- [ ] Ability to add a word on definition from hanzi questions

#### Allow users to add words to their list
- [X] Page to display vocabulary and search within vocabulary
- [ ] Add notes to user vocabulary (not super necessary, can be a fast follow)

#### Quiz page
- [ ] handle case in which a user has nothing to quiz
- [X] add grammar rules to quiz page

#### Bugs to fix
- [X] Pinyin search should allow for both numbered and actual pinyin
- [x] Frontend should display accents not as numbers
- [X] Enter should work on forms
- [ ] Infra: frontend doesn't always rerender (fast follow)
- [X] Word search results should include user vocabulary ID
- [ ] If there has been a change to user vocabulary or user grammar rules, buttons should change to refresh
- [ ] Searching two numeric forms without a space in between does not yield results (i.e. zheng4zai4 vs zheng4 zai4)

#### Tech Debt
- [X] Clean up search endpoint for grammar rules using nested serializers
- [X] See if you can clean up grammar rule examples

#### Add Stripe Payments
- [X] redirect to Stripe payment dashboard
- [X] webhook for continuing payments
- [X] spooler job to check expiring payments

#### Deployment
- [ ] create production Dockerfile for web and postgres
- [ ] create production uwsgi config
- [ ] remove all migrations and re-run makemigrations
- [ ] write scripts to setup ufw on servers
- [ ] write nginx configuration and use certbot (steal from Babblegraph)

#### Wishlist
- [ ] Search without accents (fast follow)

## Progress 06/25/2023-07/02/2023

#### 07/01/2023
- [X] Make next question button work
- [X] Fix bug: form resets when user submits an answer

#### 06/30/2023
- [X] style quiz page

## Progress 06/18/2023-06/24/2023


#### 06/23/2023
- [X] add style to user grammar rules
- [X] Add/Remove buttons to user grammar rules
- [X] add link to quiz page

#### 06/22/2023
- [X] Add pagination to word search
- [X] Word search results should include user vocabulary ID

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
