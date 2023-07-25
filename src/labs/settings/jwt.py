""" JWT Settings

"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.types import SecretStr


class JWTSettings(BaseSettings):

    # Secrets that the application requires for session
    # and cross domain checking
    secret_key: SecretStr
    algorithm: str = "HS256"

    model_config = SettingsConfigDict(
        env_prefix="JWT_",
    )
