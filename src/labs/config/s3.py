""" S3 Bucket configuration for the application

An application may require to store files in a remote location. This
configuration allows the application to define the S3 bucket. An 
application may have more than one bucket.
"""
from pydantic import BaseSettings
from pydantic.types import SecretStr

class S3BucketSettings(BaseSettings):

    endpoint: str
    bucket_name: str
    port: int = 443 # Overriden for development
    access_key: SecretStr
    secret_key: SecretStr
    region: str = "ap-south-1" # Set to Linode Singapore
    tls: bool = True # See docs on using SSL in development
