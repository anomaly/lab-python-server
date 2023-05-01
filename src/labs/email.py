"""" Redmail based email helper functions

Refer to documentation for samples, this package essentially providers
what the db or config provide for database environments.

Importing this should give you a email sender configured to send emails
and load templates from the templates folder.

Redmail docs are located at https://red-mail.readthedocs.io/
"""
import os
from redmail import EmailSender

from .config import config

sender = EmailSender(
    host=config.SMTP_HOST,
    port=config.SMTP_PORT,
    username=config.SMTP_USER.get_secret_value(),
    password=config.SMTP_PASSWORD.get_secret_value(),
    use_starttls=False,
)

# Compute the path relative to this script and append "templates"
script_path = os.path.dirname(os.path.abspath(__file__))
templates_path = os.path.join(script_path, "templates")

sender.set_template_paths(
    html=os.path.join(templates_path, "html"),
    text=os.path.join(templates_path, "text")
)