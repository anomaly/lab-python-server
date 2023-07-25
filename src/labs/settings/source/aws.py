""" AWS Secrets Manager Source

This is a custom source for pydantic settings that will read from
AWS Secrets Manager. There are some particulars that make the
scenario a little more complex than a simple environment variable.

S3 bucket names have to be unique across a region, to facilitate this
use we a hash appended to the bucket name, this makes it impossible
for us to know the bucket name at build time.

RDS will only provision an admin user, however the application should
not use these credentials and AWS will not make these credentials available
to the EKS cluster. We create a user and password which will end up being
the credentials used by the application, the user is created post
infrastructure deployment by another process.

Finally to reduce the number of secrets written (AWS charged per secret)
so values are written into the same secret, this means that the source
has to undo them and make them available as if they were environment variables.

Secrets Manager also recommends using a caching layer so we aren't hitting
the service on every requests. This is achieved using an official caching
plugin maintained by AWS for Boto3.

kubernetescluster_rds_aurora_access_details
kubernetescluster_s3_buckets
kubernetescluster_redis_cluster_endpoint
kubernetescluster_mq_broker_access_details

{
	"cluster_endpoint": "kubernetescluster-aurora-cluster.cluster-cc3gsmhcmobl.ap-southeast-2.rds.amazonaws.com",
	"username": "kubernetescluster",
	"password": "randomstring"
}
{
	"s3_bucket_media": "kubernetescluster.media.b4ea46e2a43cc218",
	"s3_bucket_ugc": "kubernetescluster.ugc.b4ea46e2a43cc218"
}
{
	"cluster_endpoint": "kubernetescluster-redis.vfen35.0001.apse2.cache.amazonaws.com"
}

{
	"username": "ExampleUser",
	"password": "randomstring",
	"endpoint": "amqp+ssl://b-40a3474a-af07-4a04-9c73-24fd6b4adab6-1.mq.ap-southeast-2.amazonaws.com:5671"
}
"""

from typing import (
    Any,
    Type,
    Tuple
)

import botocore
import botocore.session
from aws_secretsmanager_caching import (
    SecretCache,
    SecretCacheConfig
)

from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    PydanticBaseSettingsSource
)

cache_config = SecretCacheConfig()  # See below for defaults
cache = SecretCache(config=cache_config, client=client)

paginator = client.get_paginator('list_secrets')
for page in paginator.paginate():
    for secret in page['SecretList']:
        # print(cache.get_secret_string(secret['Name']))
        print(secret['Name'])


class AWSSecretsManagerSource(EnvSettingsSource):
    """

    """

    KEY_PREFIX = "kubernetescluster_"

    def __init__(
        self,
        settings_cls: type[BaseSettings],
    ) -> None:

        super().__init__(settings_cls)

        session = botocore.session.get_session()
        self.secretsmanager_client = session.create_client(
            'secretsmanager',
            region_name='ap-southeast-2'
        )

        # Cache configuration with default values see following for options
        # https://github.com/aws/aws-secretsmanager-caching-python#cache-configuration
        cache_config = SecretCacheConfig()

        self.secrets_cache = SecretCache(
            config=cache_config,
            client=self.secretsmanager_client
        )

        print("works")

    def get_field_value(
            self,
            field: FieldInfo,
            field_name: str
    ):
        if field_name == "db":
            return "localhost", field_name, False

    def _get_rds_value(self, field_name: str):
        pass

    def _get_mq_value(self, field_name: str):
        pass

    def _get_s3_value(self, field_name: str):
        pass


class AWSSecretsManagerSourceMixin(BaseSettings):
    """


    """

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:

        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            AWSSecretsManagerSource(settings_cls)
        )
