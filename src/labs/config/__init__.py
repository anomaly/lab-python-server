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

    # AMQP compatible configuration
    amqp: AMQPSettings = AMQPSettings()

    # TaskIQ writes results to a Redis database
    redis: RedisSettings = RedisSettings()

    lifetime: LifetimeSettings = LifetimeSettings()

    # Communication related configuration
    smtp: SMTPSettings = SMTPSettings()
    sms: SMSGatewaySettings = SMSGatewaySettings()

    # Secrets that the application requires for session
    jwt: JWTSettings = JWTSettings()

    # Overrides for FastAPI root router, the aim of this
    # is so that the template can maintain api.py
    api_router: APIRouterSettings = APIRouterSettings()

    
# A singleton instance of the configuration
config = Config()

