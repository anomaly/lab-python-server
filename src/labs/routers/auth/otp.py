""" Reference implementation of OTP authentication. 

"""

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...utils.auth import create_access_token

from ...db import get_async_session
from ...models import User
from ...config import config

from ...schema import OTPTriggerEmailRequest, \
  OTPTriggerSMSRequest, OTPVerifyRequest, OTPTriggerResponse,\
  Token

router = APIRouter()

@router.post(
    "/initiate/email",
)
async def initiate_otp_email(
  request: OTPTriggerEmailRequest, 
  session: AsyncSession = Depends(get_async_session)
) -> OTPTriggerResponse:
  """ Attempt to authenticate a user and issue JWT token

    The user has provided us their email address and we will
    attempt to authenticate them via OTP.
  
  """
  # Get the user account
  user = await User.get_by_email(session, request.email)

  if user is None:
    user = await User.create(session, **request.dict())

  # If not found make a user account with the mobile

  # Initiate the OTP process

  return OTPTriggerResponse(success=True)


@router.post(
  "/initiate/sms",
)
async def initiate_otp_sms(request: OTPTriggerSMSRequest, 
  session: AsyncSession = Depends(get_async_session)
) -> OTPTriggerResponse:
  """ Attempt to authenticate a user and issue JWT token

    The user has provided a mobile number and we will text them
    their OTP and let them login. 
  
  """
  # Get the user account
  user = await User.get_by_phone(session, request.mobile_number)

  # If not found make a user account with the mobile
  if user is None:
    user = await User.create(session, **request.dict())

  # Initiate the OTP process

  return OTPTriggerResponse(success=True)

@router.post("/verify")
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
