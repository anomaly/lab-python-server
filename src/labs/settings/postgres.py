""" Postgres database configuration

Anomaly projects typically use a PostgreSQL database to store data. This
configuration allows the application to define the database connection 
and can either be a container or a hosted product by a cloud provider.
"""
from pydantic import BaseSettings, PostgresDsn
from pydantic.types import SecretStr

class PostgresSettings(BaseSettings):

    # Configuration required to construct the Postgres DSN
    db: str
    user: str
    password: SecretStr
    host: str
    port: int = 5432

    @property
    def async_dsn(self) -> PostgresDsn:
        """Construct the Postgres DSN from the configuration

          This uses the async driver for asyncio based operations in
          SQLAlchemy
        """
        db_url = "".join([
            "postgresql+asyncpg://",
            self.user,
            ":",
            self.password.get_secret_value(),
            "@",
            self.host,
            ":",
            str(self.port),
            "/",
            self.db])

        return PostgresDsn(
            url=db_url,
            scheme="postgresql+asyncpg",
            user=self.user,
            password=self.password,
        )

    class Config:
        """ Env vars are prefixed with POSTGRES_ are loaded
        into instances of this class
        """
        env_prefix = "POSTGRES_"
