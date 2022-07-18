from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class OTPTriggerRequest(BaseModel):
    phone_number: str

class OTPVerifyRequest(BaseModel):
    otp: str

class AuthResponse(BaseModel):
    """Response from the authentication endpoint
    """
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
