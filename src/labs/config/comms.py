""" Communication related configuration.

SMTP is the generic way to send emails. This configuration allows the
application to define the SMTP server and credentials.

By default we should always think about supporting TLS.
"""

from pydantic import BaseSettings
from pydantic.types import SecretStr


class SMTPSettings(BaseSettings):

    host: str
    port: int = 587
    user: SecretStr
    password: SecretStr
    start_tls: bool = True

    class Config:
        """ Env vars are prefixed with SMTP_ are loaded
        into instances of this class
        """
        env_prefix = "SMTP_"

class SMSGatewaySettings(BaseSettings):

    api_id: SecretStr
    api_secret: SecretStr
    text_from: str

    class Config:
        """ Env vars are prefixed with SMS_ are loaded
        into instances of this class
        """
        env_prefix = "SMS_"
