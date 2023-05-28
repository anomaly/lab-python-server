""" Configuration for the application

"""

from pydantic import BaseSettings
from pydantic.types import SecretStr

from .postgres import PostgresSettings
from .s3 import S3BucketSettings
from .ampq import AMPQSettings
from .redis import RedisSettings
from .comms import SMTPSettings, SMSGatewaySettings

class Config(BaseSettings):
    """Configuration for the application

    The following values are read from the container environment, it's
    provided via a configuration file or a secret management system
    depending on the environment.
    """

    # Environment the application is running in
    env: str = "prod"

    # Postgres database configuration for the application
    db: PostgresSettings = PostgresSettings()

    # S3 Bucket configuration for the application
    storage: S3BucketSettings = S3BucketSettings()

    # AMPQ compatible configuration
    ampq: AMPQSettings = AMPQSettings()

    # TaskIQ writes results to a Redis database
    redis: RedisSettings = RedisSettings()

    # Communication related configuration
    # smtp: SMTPSettings = SMTPSettings()
    # sms: SMSGatewaySettings = SMSGatewaySettings()
    
    # Secrets that the application requires for session
    # and cross domain checking
    # JWT_SECRET_KEY: SecretStr
    # JWT_ALGORITHM: str = "HS256"

    # EMAIL_FROM: str


    # How many times should a task be retried by default
    # APP_QUEUE_RETRY_COUNT: int = 3

    
    
# A singleton instance of the configuration
config = Config()

