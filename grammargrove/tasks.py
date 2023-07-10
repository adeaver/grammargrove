from typing import List

import django

import os
import logging
import uuid
from functools import wraps

logger = logging.getLogger(__name__)

try:
    from uwsgidecorators import spool, cron

    django.setup()

    @cron(10, -1, -1, -1, -1)
    def start_grammar_rule_fetches(num):
        from grammarrules.models import GrammarRule
        from grammarrules.examples import (
            is_over_daily_usage_limit,
            get_best_candidate_grammar_rules_for_examples
        )
        if is_over_daily_usage_limit():
            logging.warn(f"ChatGPT usage is over the daily limit, skipping")
            return
        if os.environ.get("ENABLE_GRAMMAR_FETCHES", "false") != "true":
            logging.warn("Grammar fetching job is disabled")
            return
        rules: List[GrammarRule] = (
            get_best_candidate_grammar_rules_for_examples()
        )
        for r in rules:
            logging.warn(f"Enqueuing grammar rule {r.id}")
            fetch_examples_for_grammar_rule(str(r.id))


    @cron(15, -1, -1, -1, -1)
    def create_practice_reminders(num):
        from users.practice_emails import create_all_practice_emails
        logging.warn("Creating outstanding practice reminders")
        create_all_practice_emails()


    @cron(8, -1, -1, -1, -1)
    def send_outstanding_practice_reminders(num):
        from users.practice_emails import send_outstanding_practice_reminders
        logging.warn("Sending outstanding practice reminders")
        send_outstanding_practice_reminders()


    logger.warning("Imported spool successfully.")
except Exception:
    logger.warning("Couldn't import spool.")

    def spool(pass_arguments):
        def decorator(method):
            if callable(pass_arguments):
                method.gw_method = method.__name__
            else:
                method.gw_method = pass_arguments

            @wraps(method)
            def wrapper(*args, **kwargs):
                method(*args, **kwargs)

            return wrapper

        if callable(pass_arguments):
            return decorator(pass_arguments)
        return decorator


@spool(pass_arguments=True)
def send_login_email(login_email_id: str):
    import uwsgi
    from users.utils import send_login_email_to_user, send_verifcation_email_to_user
    from users.models import UserLoginEmail, UserLoginEmailType
    try:
        login_emails = UserLoginEmail.objects.filter(pk=uuid.UUID(login_email_id))
        retryable = False
        if not login_emails:
            logging.info(f"{login_email_id} is invalid, skipping")
            return uwsgi.SPOOL_OK
        email = login_emails[0]
        if email.is_expired():
            logging.info(f"UserLoginEmail {login_email_id} is expired, skipping")
            return uwsgi.SPOOL_OK
        elif email.is_fulfilled():
            logging.info(f"UserLoginEmail {login_email_id} is already fulfilled, skipping")
            return uwsgi.SPOOL_OK
        elif email.email_type == UserLoginEmailType.LOGIN:
            retryable = send_login_email_to_user(email)
        elif email.email_type == UserLoginEmailType.VERIFICATION:
            retryable = send_verifcation_email_to_user(email)
        if retryable:
            return uwsgi.SPOOL_RETRY
        email.fulfilled = True
        email.save()
        return uwsgi.SPOOL_OK
    except:
        return uwsgi.SPOOL_RETRY


@spool(pass_arguments=True)
def fetch_examples_for_grammar_rule(grammar_rule_id: str):
    import uwsgi
    from grammarrules.examples import fetch_grammar_rule_examples
    from grammarrules.examples import is_over_daily_usage_limit
    logging.warn(f"Fetching examples for rule {grammar_rule_id}")
    try:
        if is_over_daily_usage_limit():
            logging.warn(f"ChatGPT usage is over the daily limit, skipping")
            return uwsgi.SPOOL_OK
        example_prompt_id = fetch_grammar_rule_examples(grammar_rule_id, valid_hsk_levels=[1, 2])
        parse_grammar_rule_example(example_prompt_id)
        logging.warn(f"Fetched examples for rule {grammar_rule_id}")
    except Exception as e:
        logging.warn(f"Got exception {e}")
    return uwsgi.SPOOL_OK

@spool(pass_arguments=True)
def parse_grammar_rule_example(grammar_rule_example_id: str):
    import uwsgi
    from grammarrules.parse import parse_example_prompt
    logging.warn(f"Parsing example {grammar_rule_example_id}")
    try:
        parse_example_prompt(grammar_rule_example_id)
        logging.warn(f"Parsed example {grammar_rule_example_id}")
    except Exception as e:
        logging.warn(f"Got exception {e}")
    return uwsgi.SPOOL_OK
