""" Verification related endpoints for accounts and OTP


"""
from fastapi import APIRouter, Depends,\
  HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...utils.auth import create_access_token

from ...db import get_async_session
from ...config import config

from ...models.user import User
from ...schema.auth import VerifyAccountRequest, OTPVerifyRequest,\
  Token


router = APIRouter()

@router.post(
  "/account", 
  status_code=status.HTTP_202_ACCEPTED
)
async def verify_user(
  request: VerifyAccountRequest,
  session: AsyncSession = Depends(get_async_session),
):
    """
    Verify an account using a one time token

    The signup process would have emailed the user a one time activation
    token, pass this token to the user object and we can ask the account
    to be set as verified.

    If the token is invalid, or was never generated an obscure error 
    message is to be sent back to the client, so we don't reveal that
    the token or accounts status is valid
    """
    user = await User.get_by_email(
       session, 
       request.email
    )

     # Even if there's an error we aren't going to reveal the
     # fact that the user exists or not
    if not user:
      raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
      )
    
    verification_outcome = await user.verify_user_account(
      session, 
      request.token
    )

    if not verification_outcome:
      raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Verification failed" 
      )

@router.post("/otp")
async def verify_otp(
  request: OTPVerifyRequest, 
  session: AsyncSession = Depends(get_async_session)
):
  """ Attempt to authenticate a user and issue JWT token
  
  """
  # Get the user account
  user = await User.get_by_phone(session, request.mobile_number)

  if not user:
    raise HTTPException(status_code=401, detail="Invalid mobile number")

  if not user.verify_otp(
    config.APP_TOTP_INTERVAL, 
    config.APP_TOTP_WINDOW,
    request.otp
  ):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect OTP",
      headers={"WWW-Authenticate": "Bearer"},
    )

  access_token = create_access_token(
    subject=str(user.id),
    fresh=True
  )
  
  return Token(
    access_token=access_token,
    token_type="bearer"
  )
