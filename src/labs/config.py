"""Configuration for the application

"""

from pydantic import BaseSettings, PostgresDsn, RedisDsn, AmqpDsn
from pydantic.types import SecretStr

class Config(BaseSettings):
    """Configuration for the application

    The following values are read from the container environment, it's
    provided via a configuration file or a secret management system
    depending on the environment.
    """
    
    # Configuration required to construct the Postgres DSN
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432

    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: SecretStr
    RABBITMQ_NODE_PORT: int = 5672
    RABBITMQ_HOST: str

    # redis is used by celery for workers
    REDIS_HOST: str
    REDIS_PORT: int = 6379

    # S3 related configuration
    S3_ENDPOINT: str
    S3_BUCKET_NAME: str
    S3_PORT: int = 443 # Overriden for development
    S3_ACCESS_KEY: SecretStr
    S3_SECRET_KEY: SecretStr
    S3_REGION: str = "ap-south-1" # Set to Linode Singapore
    S3_USE_SSL: bool = True # See docs on using SSL in development

    S3_UPLOAD_EXPIRY: int = 5 # In minutes
    S3_DOWNLOAD_EXPIRY: int = 5 # In minutes

    # Secrets that the application requires for session
    # and cross domain checking
    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # SMTP and SMS related configuration
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USER: SecretStr
    SMTP_PASSWORD: SecretStr
    
    SMS_API_KEY: SecretStr
    SMS_API_SECRET: SecretStr
    SMS_FROM: str

    # The following are recommended values for the app to use for
    # security tokens, and other cryptography related features.
    # 
    # While these can be overridden in the container environment,
    # it's recommend that you use the values below.

    APP_VERIFICATION_TOKEN_EXPIRY: int = 600 # In seconds
    APP_TOTP_NUM_DIGITS: int = 6 # Login code length
    APP_TOTP_INTERVAL: int = 30 # How long is a token valid
    APP_TOTP_WINDOW: int = 30 # How far off can you drift


    @property
    def postgres_async_dsn(self) -> PostgresDsn:
        """Construct the Postgres DSN from the configuration

          This uses the async driver for asyncio based operations in
          SQLAlchemy
        """
        db_url = "".join([
            "postgresql+asyncpg://",
            self.POSTGRES_USER,
            ":",
            self.POSTGRES_PASSWORD.get_secret_value(),
            "@",
            self.POSTGRES_HOST,
            ":",
            str(self.POSTGRES_PORT),
            "/",
            self.POSTGRES_DB])

        return PostgresDsn(
            url=db_url,
            scheme="postgresql+asyncpg",
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
        )

    @property
    def redis_dsn(self) -> RedisDsn:
        """Construct the DSN for the celery broker
        """
        redis_url=f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'
        return RedisDsn(
            url=redis_url, 
            scheme="redis"
        )
    
    @property
    def amqp_dsn(self) -> AmqpDsn:
        amqp_url = "".join([
            "amqp://",
            self.RABBITMQ_DEFAULT_USER,
            ":",
            self.RABBITMQ_DEFAULT_PASS.get_secret_value(),
            "@",
            self.RABBITMQ_HOST,
            ":",
            str(self.RABBITMQ_NODE_PORT),
        ])
        return AmqpDsn(
            url=amqp_url, 
            scheme="amqp",
            user=self.RABBITMQ_DEFAULT_USER,
            password=self.RABBITMQ_DEFAULT_PASS,
        )
    
# A singleton instance of the configuration
config = Config()

