"""Configuration for the application

"""

from pydantic import BaseModel, BaseSettings, PostgresDsn

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

    # fluentd configuration
    FLUENTD_HOST: str
    FLUENTD_PORT: int

    # Secrets that the application requires for session
    # and cross domain checking
    CSRF_SECRET: str

    @property
    def postgres_dsn(self) -> PostgresDsn:
        """Construct the Postgres DSN from the configuration
        """
        return PostgresDsn(
            database=self.POSTGRES_DB,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
        )

# A singleton instance of the configuration
config = Config()

class CsrfConfig(BaseModel):
  """A model required by the CSRF protection plugin

  The FastAPI initialiser registers a decorated instance.
  """
  secret_key:str = config.CSRF_SECRET
