""" Configuration for the application

"""

from pydantic import BaseSettings

from .postgres import PostgresSettings
from .s3 import S3BucketSettings
from .amqp import AMQPSettings
from .redis import RedisSettings
from .comms import SMTPSettings, SMSGatewaySettings
from .lifetime import LifetimeSettings
from .jwt import JWTSettings
from .api_router import APIRouterSettings
from .verbosity import VerbositySettings

class Settings(BaseSettings):
    """Configuration for the application

    The following values are read from the container environment, it's
    provided via a configuration file or a secret management system
    depending on the environment.

    Note: pydatic sub models allows for the configuration to be
    broken up into classes, it will convert uppercase environment
    variables into lower case python variables and take prefixes
    and break it into sub models.

    e.g DB_HOST will be converted to db.host

    There are many variables that default values assigned and are not
    required to be set in the environment.
    """

    # Environment the application is running in
    env: str = "prod"

    # Postgres database configuration for the application
    db: PostgresSettings = PostgresSettings()

    # S3 Bucket configuration for the application
    storage: S3BucketSettings = S3BucketSettings()

    # AMQP compatible configuration
    amqp: AMQPSettings = AMQPSettings()

    # TaskIQ writes results to a Redis database
    redis: RedisSettings = RedisSettings()

    # Communication related configuration
    smtp: SMTPSettings = SMTPSettings()
    sms: SMSGatewaySettings = SMSGatewaySettings()

    # Secrets that the application requires for session
    jwt: JWTSettings = JWTSettings()

    # Overrides for FastAPI root router, the aim of this
    # is so that the template can maintain api.py
    api_router: APIRouterSettings = APIRouterSettings()

    # Lifetime of various security related items
    lifetime: LifetimeSettings = LifetimeSettings()

    # Verbosity of various tokens
    verbosity: VerbositySettings = VerbositySettings()

    
# A singleton instance of the configuration
settings: Settings = Settings()

