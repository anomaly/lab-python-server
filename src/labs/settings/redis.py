""" Redis configuration for TaskIQ

TaskIQ writes the results of the task to a Redis database. This
configuration allows the application to define the Redis database
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.networks import RedisDsn, Url, UrlConstraints


class RedisSettings(BaseSettings):

    # redis is used by TaskIQ for writing results
    host: str
    port: int = 6379

    @property
    def dsn(self) -> RedisDsn:
        """Construct the DSN for the TaskIQ broker

        This is provided by a container for development, but you 
        can choose to use a hosted product in production.
        """
        redis_url = f'redis://{self.host}:{self.port}'

        return RedisDsn(
            Url(redis_url),
        )

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
    )
