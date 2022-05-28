"""Configuration for the application

"""

from pydantic import BaseSettings, PostgresDsn

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