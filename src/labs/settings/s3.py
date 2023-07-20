""" S3 Bucket configuration for the application

An application may require to store files in a remote location. This
configuration allows the application to define the S3 bucket. An 
application may have more than one bucket.
"""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.types import SecretStr


class S3BucketSettings(BaseSettings):

    endpoint: str
    bucket_name: str
    port: int = 443  # Overriden for development
    access_key: Optional[SecretStr]
    secret_key: Optional[SecretStr]
    region: str = "ap-south-1"  # Set to Linode Singapore
    tls: bool = True  # See docs on using SSL in development

    model_config = SettingsConfigDict(
        env_prefix="S3_",
    )
