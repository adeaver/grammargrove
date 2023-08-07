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

    @cron(-1, -1, -1, -1, -1)
    def scavenge_unparsed_examples(num):
        from grammarrules.parse import get_unparsed_examples
        from grammarrules.validate import get_grammar_rules_to_validate
        from ops.featureflags import FeatureFlags
        from django.db import close_old_connections
        close_old_connections()
        if FeatureFlags.GrammarRuleScavengerEnabled.flag().get():
            unparsed_examples = get_unparsed_examples()
            logging.warn(f"Scavenging {len(unparsed_examples)} examples")
            for example in unparsed_examples:
                parse_grammar_rule_example.spool({
                    b"grammar_rule_example_id": str(example.grammar_rule_example_prompt.id).encode("utf-8"),
                    b"grammar_rule_example_line_idx": str(example.line_idx).encode("utf-8")
                })
        else:
            logging.warning("Grammar rule example scavenger is disabled")
        if FeatureFlags.GrammarRuleValidationEnabled.flag().get():
            grammar_rules_to_validate = get_grammar_rules_to_validate(
                limit=FeatureFlags.NumberOfValidationExamplesPerCycle.flag().get()
            )
            do_validation_for_grammar_rule_examples.spool({
                b"grammar_rule_example_ids": ",".join(grammar_rules_to_validate).encode("utf-8")
            })
        else:
            logging.warning("Grammar rule example validation scavenger is disabled")


    @cron(10, -1, -1, -1, -1)
    def start_grammar_rule_fetches(num):
        from ops.featureflags import FeatureFlags
        from grammarrules.models import GrammarRule
        from grammarrules.examples import (
            is_over_daily_usage_limit,
            get_best_candidate_grammar_rules_for_examples
        )
        from django.db import close_old_connections
        close_old_connections()
        if is_over_daily_usage_limit():
            logging.warn(f"ChatGPT usage is over the daily limit, skipping")
            return
        if not FeatureFlags.GrammarRuleFetchesEnabled.flag().get():
            logging.warn("Grammar fetching job is disabled")
            return
        rules: List[GrammarRule] = (
            get_best_candidate_grammar_rules_for_examples()
        )
        for r in rules:
            logging.warn(f"Enqueuing grammar rule {r.id}")
            fetch_examples_for_grammar_rule.spool({
                b"grammar_rule_id": str(r.id).encode("utf-8")
            })


    @cron(15, -1, -1, -1, -1)
    def create_practice_reminders(num):
        from users.practice_emails import create_all_practice_emails
        from django.db import close_old_connections
        close_old_connections()
        logging.warn("Creating outstanding practice reminders")
        create_all_practice_emails()

    @cron(8, -1, -1, -1, -1)
    def send_outstanding_practice_reminders(num):
        from users.practice_emails import send_outstanding_practice_reminders
        from django.db import close_old_connections
        close_old_connections()
        logging.warn("Sending outstanding practice reminders")
        send_outstanding_practice_reminders()

    @cron(-1, -1, -1, -1, -1)
    def send_outstanding_login_emails(num):
        from users.login_emails import get_outstanding_login_emails
        from django.db import close_old_connections
        close_old_connections()
        logging.warn("Sending outstanding login emails")
        login_email_ids = get_outstanding_login_emails()
        for email in login_email_ids:
            logging.warning(f"Spooling ID {email}")
            fulfill_login_email.spool({ "login_email_id".encode("utf-8"): str(email).encode("utf-8") })



    @cron(-5, -1, -1, -1, -1)
    def do_ops_ping(num):
        # This is a quick test that spooler, nginx, and the db are all running
        from ops.utils import register_ping
        from django.db import close_old_connections
        close_old_connections()
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
    from django.db import close_old_connections
    close_old_connections()
    key = b"login_email_id"
    if key not in args:
        logging.warning(f"Key is not in args")
        return uwsgi.SPOOL_OK
    login_email_id = args[key].decode("utf-8")
    fulfill_login_email_by_id(UUID(login_email_id))


@spool(pass_arguments=True)
def fetch_examples_for_grammar_rule(args: Dict[str, str]):
    import uwsgi
    from grammarrules.examples import (
        fetch_grammar_rule_examples,
        is_over_daily_usage_limit,
        get_best_target_hsk_level_for_grammar_rule
    )
    from django.db import close_old_connections
    close_old_connections()
    key = b"grammar_rule_id"
    if key not in args:
        logging.warning("key is not in args")
        return uwsgi.SPOOL_OK
    grammar_rule_id = args[key].decode("utf-8")
    logging.warn(f"Fetching examples for rule {grammar_rule_id}")
    try:
        if is_over_daily_usage_limit():
            logging.warn(f"ChatGPT usage is over the daily limit, skipping")
            return uwsgi.SPOOL_OK
        valid_hsk_levels = get_best_target_hsk_level_for_grammar_rule(grammar_rule_id)
        example_prompt_id = fetch_grammar_rule_examples(grammar_rule_id, valid_hsk_levels=valid_hsk_levels)
        parse_grammar_rule_example.spool({
            b"grammar_rule_example_id": str(example_prompt_id).encode("utf-8")
        })
        logging.warn(f"Fetched examples for rule {grammar_rule_id}")
    except Exception as e:
        logging.warn(f"Got exception {e}")
    return uwsgi.SPOOL_OK

@spool(pass_arguments=True)
def parse_grammar_rule_example(args: Dict[str, str]):
    import uwsgi
    from grammarrules.parse import (
        parse_example_prompt,
        reparse_example_prompt_line_number
    )
    from django.db import close_old_connections
    close_old_connections()
    key = b"grammar_rule_example_id"
    if key not in args:
        logging.warning("key is not in args")
        return uwsgi.SPOOL_OK
    grammar_rule_example_id = args[key].decode("utf-8")
    line_idx_key = b"grammar_rule_example_line_idx"
    line_idx = args.get(line_idx_key)
    if line_idx is None:
        logging.warn(f"Parsing example {grammar_rule_example_id}")
        try:
            parse_example_prompt(grammar_rule_example_id)
            logging.warn(f"Parsed example {grammar_rule_example_id}")
        except Exception as e:
            logging.warn(f"Got exception {e}")
        return uwsgi.SPOOL_OK
    else:
        logging.warn(f"Parsing line {line_idx} for example {grammar_rule_example_id}")
        try:
            line_idx = int(line_idx.decode("utf-8"))
            reparse_example_prompt_line_number(grammar_rule_example_id, line_idx)
            logging.warn(f"Reparsed example {grammar_rule_example_id}")
        except Exception as e:
            logging.warn(f"Got exception {e}")
        return uwsgi.SPOOL_OK


@spool(pass_arguments=True)
def do_validation_for_grammar_rule_examples(args: Dict[str, str]):
    import uwsgi
    from grammarrules.validate import (
        validate_grammar_rule_examples
    )
    from ops.featureflags import FeatureFlags
    from django.db import close_old_connections
    close_old_connections()
    if not FeatureFlags.GrammarRuleValidationEnabled.flag().get():
        logging.warning("Validation is not enabled")
        return uwsgi.SPOOL_OK
    key = b"grammar_rule_example_ids"
    if key not in args:
        logging.warning("key is not in args")
        return uwsgi.SPOOL_OK
    grammar_rule_example_ids = args[key].decode("utf-8").split(",")
    try:
        logging.warn(f"Validating examples {grammar_rule_example_ids}")
        validate_grammar_rule_examples(grammar_rule_example_ids)
        logging.warn(f"Validated examples {grammar_rule_example_ids}")
    except Exception as e:
        logging.warn(f"Got exception {e}")
    return uwsgi.SPOOL_OK

