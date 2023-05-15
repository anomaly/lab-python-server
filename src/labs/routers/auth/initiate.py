
"""
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_async_session
from ...models import User
from ...config import config

from ...schema.auth import OTPTriggerEmailRequest, \
  OTPTriggerSMSRequest, InitiateResetPasswordRequest

from .tasks import send_reset_password_email

router = APIRouter()

@router.post(
    "/otp/email",
)
async def initiate_otp_email(
  request: OTPTriggerEmailRequest, 
  session: AsyncSession = Depends(get_async_session)
):
  """ Attempt to authenticate a user and issue JWT token

    The user has provided us their email address and we will
    attempt to authenticate them via OTP.
  
  """
  # Get the user account
  user = await User.get_by_email(session, request.email)

  # Create the user with a random base32 password
  # this will obviously be unusable by the user
  # if they wish to login via a password then they will have
  # to follow the reset_password flow
  if user is None:
    from pyotp import random_base32
    user = await User.create(
      session,
      email=request.email,
      password=random_base32()
    )

  # Initiate the OTP process as a background task
  await send_otp_email.kiq(user.id)

@router.post(
  "/otp/sms",
)
async def initiate_otp_sms(request: OTPTriggerSMSRequest, 
  session: AsyncSession = Depends(get_async_session)
):
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



@router.post(
    "/password/reset",
    status_code=status.HTTP_202_ACCEPTED
)
async def initiate_password_reset(
    request: InitiateResetPasswordRequest,
    session: AsyncSession = Depends(get_async_session),
):
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
        
    # Queue a task to send the verification email
    await send_reset_password_email.kiq(user.id)
