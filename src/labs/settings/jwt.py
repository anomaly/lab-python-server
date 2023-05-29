""" JWT Settings

"""

from pydantic import BaseSettings
from pydantic.types import SecretStr

class JWTSettings(BaseSettings):

    # Secrets that the application requires for session
    # and cross domain checking
    secret_key: SecretStr
    algorithm: str = "HS256"


    class Config:
        """ Env vars are prefixed with JWT_ are loaded
        into instances of this class
        """
        env_prefix = "JWT_"
