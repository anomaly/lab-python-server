""" Verbosity of various security tokens 

These settings are the verbosity of various security related items
such as tokens, and links. These are the recommend settings based
on your research.
"""

from pydantic import BaseSettings

class VerbositySettings(BaseSettings):

    totp: int = 6 # Login code length

    verification_token: int = 32 # Signup verification code
    reset_password_token: int = 32 # Reset password code

