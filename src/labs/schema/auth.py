from .utils import AppBaseModel
class PasswordLoginRequest(AppBaseModel):
    """ Requires parameters to login via password
    """
    username: str
    password: str

class SignupRequest(AppBaseModel):
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

class AuthResponse(AppBaseModel):
    """Response from the authentication endpoint
    """
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
