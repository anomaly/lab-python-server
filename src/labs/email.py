"""" Redmail based email helper functions

Refer to documentation for samples, this package essentially providers
what the db or config provide for database environments.

Importing this should give you a email sender configured to send emails
and load templates from the templates folder.

the sender is set to config.EMAIL_FROM so each call does not have to
reference the configuration and can simply provide the template information

> Note: you can however override the sender per call if you so wish to

Redmail docs are located at https://red-mail.readthedocs.io/
"""
import os
from redmail.email.sender import EmailSender

from .settings import settings

# Custom factory to be able to set the sender globally
class EmailSenderFactory(EmailSender):
    @property
    def sender(self):
        return self._sender
    
    @sender.setter
    def sender(self, sender: str):
        self._sender = sender


sender = EmailSenderFactory(
    host=settings.smtp.host,
    port=settings.smtp.port,
    username=settings.smtp.user.get_secret_value(),
    password=settings.smtp.password.get_secret_value(),
    use_starttls=settings.smtp.start_tls,
)

# The sender is globally set so each send call does not
# have to provide this as a parameter
sender.sender=settings.smtp.mail_from

# Compute the path relative to this script and append "templates"
script_path = os.path.dirname(os.path.abspath(__file__))
templates_path = os.path.join(script_path, "templates")

sender.set_template_paths(
    html=os.path.join(templates_path, "html"),
    text=os.path.join(templates_path, "txt")
)