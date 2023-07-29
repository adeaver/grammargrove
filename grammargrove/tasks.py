from typing import Dict, List

import django

import os
import logging
import uuid
import traceback
from functools import wraps

logger = logging.getLogger(__name__)

try:
    from uwsgidecorators import spool, cron

    django.setup()

    @cron(10, -1, -1, -1, -1)
    def start_grammar_rule_fetches(num):
        from ops.featureflags import get_boolean_feature_flag
        from ops.models import FeatureFlagName
        from grammarrules.models import GrammarRule
        from grammarrules.examples import (
            is_over_daily_usage_limit,
            get_best_candidate_grammar_rules_for_examples
        )
        if is_over_daily_usage_limit():
            logging.warn(f"ChatGPT usage is over the daily limit, skipping")
            return
        if not get_boolean_feature_flag(FeatureFlagName.GrammarRuleFetchesEnabled):
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

    @cron(-1, -1, -1, -1, -1)
    def send_outstanding_login_emails(num):
        from users.login_emails import get_outstanding_login_emails
        logging.warn("Sending outstanding login emails")
        login_email_ids = get_outstanding_login_emails()
        for email in login_email_ids:
            logging.warning(f"Spooling ID {email}")
            fulfill_login_email.spool({ "login_email_id".encode("utf-8"): str(email).encode("utf-8") })



    @cron(-5, -1, -1, -1, -1)
    def do_ops_ping(num):
        # This is a quick test that spooler, nginx, and the db are all running
        from ops.utils import register_ping
        register_ping()

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
def fulfill_login_email(args: Dict[str, str]):
    from uuid import UUID
    from users.login_emails import fulfill_login_email_by_id
    key = b"login_email_id"
    if key not in args:
        logging.warning(f"Key is not in args")
        return uwsgi.SPOOL_OK
    login_email_id = args[key].decode("utf-8")
    fulfill_login_email_by_id(UUID(login_email_id))


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
