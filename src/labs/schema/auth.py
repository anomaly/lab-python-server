from pydantic import BaseModel

class PasswordLoginRequest(BaseModel):
    """ Requires parameters to login via password
    """
    username: str
    password: str

class SignupRequest(BaseModel):
    password: str
    email: str

class SignupResponse(BaseModel):
    success: bool
    email: str

class OTPTriggerEmailRequest(BaseModel):
    email: str

class OTPTriggerSMSRequest(BaseModel):
    mobile_number: str

class OTPVerifyRequest(BaseModel):
    """ OTP sent to the server to verify if it's valid """
    otp: str

class OTPTriggerResponse(BaseModel):
    """ OTP Verification result """
    success: bool

class AuthResponse(BaseModel):
    """Response from the authentication endpoint
    """
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
