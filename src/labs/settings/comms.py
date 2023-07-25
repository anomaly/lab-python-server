""" Communication related configuration.

SMTP is the generic way to send emails. This configuration allows the
application to define the SMTP server and credentials.

By default we should always think about supporting TLS.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.types import SecretStr


class SMTPSettings(BaseSettings):

    host: str
    port: int = 587
    user: SecretStr
    password: SecretStr
    start_tls: bool = True

    mail_from: str

    model_config = SettingsConfigDict(
        env_prefix="SMTP_",
    )


class SMSGatewaySettings(BaseSettings):

    api_id: SecretStr
    api_secret: SecretStr
    from_label: str

    model_config = SettingsConfigDict(
        env_prefix="SMS_",
    )
