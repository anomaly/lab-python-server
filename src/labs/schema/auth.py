from pydantic import BaseModel
from .utils import AppBaseModel

class Token(BaseModel):
    """ A model that represents a JWT token

    Used to send a newly created token or a refresh token with
    the type. For most use cases we send a bearer token.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """ A model that represents the data in a JWT token

    Literally used to validate if what we have unpacked
    is a valid token.

    """
    id: str = None


class SignupRequest(AppBaseModel):
    """ A simple request to sign up a user with an email and password    
    """
    password: str
    email: str
    first_name: str
    last_name: str

class SignupResponse(AppBaseModel):
    """  Signup Response to confirm that the email address was accepted """
    success: bool
    email: str


class VerifyAccountRequest(BaseModel):
    """ A simple request to verify a user account with a token """
    token: str
    email: str

class InitiateResetPasswordRequest(BaseModel):
    """
    A user is asking to reset their password

    This will result in a token being sent out to them which they can use
    with the following model to reset their password
    """
    email: str

class ResetPasswordRequest(BaseModel):
    """
    A request with the previously generated token and the new password
    """
    token: str
    email: str
    password: str

class OTPTriggerEmailRequest(AppBaseModel):
    """ Triggers an OTP to be sent to the user via email """
    email: str

class OTPTriggerSMSRequest(AppBaseModel):
    """ Triggers an OTP to be sent to the user via SMS """
    mobile_number: str

class OTPVerifyRequest(AppBaseModel):
    """ OTP sent to the server to verify if it's valid """
    otp: str
    mobile_number: str

