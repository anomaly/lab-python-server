from pydantic import BaseModel
from .utils import AppBaseModel

class Token(BaseModel):
    """ A model that represents a JWT token


    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """ A model that represents the data in a JWT token

    Literally used to validate if what we have unpacked
    is a valid token.

    """
    username: str = None


class SignupRequest(AppBaseModel):
    """ A simple request to sign up a user with an email and password    
    """
    password: str
    email: str

class SignupResponse(AppBaseModel):
    success: bool
    email: str

class OTPTriggerEmailRequest(AppBaseModel):
    email: str

class OTPTriggerSMSRequest(AppBaseModel):
    mobile_number: str

class OTPVerifyRequest(AppBaseModel):
    """ OTP sent to the server to verify if it's valid """
    otp: str

class OTPTriggerResponse(AppBaseModel):
    """ OTP Verification result """
    success: bool

