""" AMPQ compatible configuration

Anomaly projects use TaskIQ to manage the task queues. This configuration
allows the application to define the AMPQ connection and can either be a
container or a hosted product by a cloud provider.
"""
from pydantic import BaseSettings, AmqpDsn
from pydantic.types import SecretStr

class AMPQSettings(BaseSettings):

    # RabbitMQ is used to manage the queues
    user: str
    password: SecretStr
    port: int = 5672
    host: str

    @property
    def dsn(self) -> AmqpDsn:
        """ Construct the DSN for the AMQP broker

        This is generally used by TaskIQ to queue tasks for execution
        and is provided by a container. 

        In production you can choose to use a hosted product.
        """
        amqp_url = "".join([
            "amqp://",
            self.user,
            ":",
            self.password.get_secret_value(),
            "@",
            self.host,
            ":",
            str(self.port),
        ])
        return AmqpDsn(
            url=amqp_url, 
            scheme="amqp",
            user=self.user,
            password=self.password,
        )

    class Config:
        """ Env vars are prefixed with AMPQ_ are loaded
        into instances of this class
        """
        env_prefix = "AMPQ_"
