""" Lifetime of various security related items.

These settings are the lifetime of various security related items
such as tokens, and links. These values are in seconds.
"""

from pydantic import BaseSettings

class LifetimeSettings(BaseSettings):

    # The following are recommended values for the app to use for
    # security tokens, and other cryptography related features.
    # 
    # While these can be overridden in the container environment,
    # it's recommend that you use the values below.

    link_s3_upload: int = 300 # In seconds
    link_s3_download: int = 300 # In seconds
    
    token_jwt_access: int = 1800

    token_reset_password: int = 600 # In seconds
    token_account_verification: int = 600 # In seconds

    APP_TOTP_NUM_DIGITS: int = 6 # Login code length
    APP_TOTP_INTERVAL: int = 30 # How long is a token valid
    APP_TOTP_WINDOW: int = 30 # How far off can you drift
    