from pydantic import BaseModel

class PasswordLoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    password: str
    email: str

class OTPTriggerEmailRequest(BaseModel):
    email: str

class OTPTriggerSMSRequest(BaseModel):
    mobile_number: str

class OTPVerifyRequest(BaseModel):
    otp: str

class OTPTriggerResponse(BaseModel):
    success: bool

class AuthResponse(BaseModel):
    """Response from the authentication endpoint
    """
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
