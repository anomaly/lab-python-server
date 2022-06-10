"""Configuration for the application

"""

from functools import lru_cache
from pydantic import BaseModel, BaseSettings, PostgresDsn, RedisDsn

class Config(BaseSettings):
    """Configuration for the application

    The following values are read from the container environment, it's
    provided via a configuration file or a secret management system
    depending on the environment.
    """
    
    # Configuration required to construct the Postgres DSN
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # fluentd configuration
    FLUENTD_HOST: str
    FLUENTD_PORT: int

    # redis is used by celery for workers
    REDIS_HOST: str
    REDIS_PORT: int

    # Secrets that the application requires for session
    # and cross domain checking
    CSRF_SECRET: str

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
            self.POSTGRES_PASSWORD,
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
        return RedisDsn(url=redis_url, 
            scheme="redis")

# A singleton instance of the configuration
config = Config()

class CsrfConfig(BaseModel):
  """A model required by the CSRF protection plugin

  The FastAPI initialiser registers a decorated instance.
  """
  secret_key:str = config.CSRF_SECRET

