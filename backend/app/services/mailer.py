"""Sends the verification-code emails.

If SMTP_HOST is not set (DEMO MODE), nothing is emailed: the code is printed in the backend
window instead and the API also returns it, so the app can be demonstrated without an email account.
"""
import logging
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

from flask import current_app

from ..errors import APIError

log = logging.getLogger(__name__)

SUBJECTS = {
    "register": "Your FileAI verification code",
    "login": "Your FileAI sign-in code",
}
REASONS = {
    "register": "Use this code to confirm your email address and finish creating your FileAI account.",
    "login": "Use this code to finish signing in to FileAI. If this wasn't you, change your password.",
}


def email_configured() -> bool:
    return bool(current_app.config["SMTP_HOST"])


def send_code(email: str, name: str, code: str, purpose: str) -> bool:
    """Email the code. Returns True if it was emailed.

    Returns False only in DEMO MODE (EMAIL_DEMO_MODE=true and no SMTP_HOST): the code is then printed
    in the log and shown on screen. Without an email server and without demo mode, nothing is shown:
    the request fails, so a code can never reach someone who can't read that inbox.
    """
    cfg = current_app.config
    if not email_configured():
        if cfg["EMAIL_DEMO_MODE"]:
            log.warning("DEMO MODE (no SMTP_HOST set) - %s code for %s: %s", purpose, email, code)
            return False
        log.error("Can't send the %s code to %s: SMTP_HOST is not set in .env", purpose, email)
        raise APIError(503, "EMAIL_NOT_SET_UP", "Verification codes can't be sent because the email server "
                                                "isn't set up yet. Please contact the administrator.")

    message = EmailMessage()
    message["Subject"] = SUBJECTS[purpose]
    message["From"] = cfg["MAIL_FROM"]
    message["To"] = email
    # A proper Message-ID from the sending domain helps the email land in the inbox, not spam.
    sender_domain = (cfg["SMTP_USERNAME"] or "").partition("@")[2] or None
    message["Message-ID"] = make_msgid(domain=sender_domain)
    message["Date"] = formatdate(localtime=True)
    message.set_content(
        f"Hi {name or 'there'},\n\n{REASONS[purpose]}\n\n"
        f"    {code}\n\n"
        f"The code expires in {cfg['OTP_EXPIRES_MIN']} minutes.\n\n— FileAI"
    )
    try:
        send_message(message)
    except (OSError, smtplib.SMTPException):
        log.exception("Could not send the %s code email to %s", purpose, email)
        raise APIError(502, "EMAIL_FAILED", "We couldn't send the verification email. Please try again later.")
    log.info("Sent the %s code email to %s", purpose, email)
    return True


def send_message(message: EmailMessage) -> None:
    """Deliver one email through the configured SMTP server.

    SMTP_USE_SSL (port 465): encrypted from the first byte.
    SMTP_USE_TLS (port 587): plain connection upgraded with STARTTLS.
    Raises OSError / smtplib.SMTPException if the server can't be reached or refuses the login.
    """
    cfg = current_app.config
    context = ssl.create_default_context()
    try:
        # Python from python.org on macOS has no root certificates until "Install Certificates" is run,
        # which makes every SSL email fail. certifi (installed with the openai package) has them.
        import certifi

        context.load_verify_locations(certifi.where())
    except (ImportError, OSError):
        pass
    if cfg["SMTP_USE_SSL"]:
        smtp = smtplib.SMTP_SSL(cfg["SMTP_HOST"], cfg["SMTP_PORT"], timeout=20, context=context)
    else:
        smtp = smtplib.SMTP(cfg["SMTP_HOST"], cfg["SMTP_PORT"], timeout=20)
    with smtp:
        if not cfg["SMTP_USE_SSL"] and cfg["SMTP_USE_TLS"]:
            smtp.starttls(context=context)
        if cfg["SMTP_USERNAME"]:
            smtp.login(cfg["SMTP_USERNAME"], cfg["SMTP_PASSWORD"])
        smtp.send_message(message)
