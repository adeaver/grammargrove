import logging
import uuid
from functools import wraps

logger = logging.getLogger(__name__)

try:
    from uwsgidecorators import spool

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
