""" Reference implementation of OTP authentication. 

"""

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_async_session
from ...models import User
from ...schema import OTPTriggerEmailRequest, \
  OTPTriggerSMSRequest, OTPVerifyRequest, OTPTriggerResponse
from ...tasks.otp import initiate_otp_via_email, \
  initiate_otp_via_sms

router = APIRouter(tags=["otp"])

@router.post("/initiate/email", response_model=OTPTriggerResponse)
async def initiate_otp_request(request: OTPTriggerEmailRequest, 
  Authorize: AuthJWT = Depends(),
  session: AsyncSession = Depends(get_async_session)):
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
  initiate_otp_via_email.apply_async(args=[user.id])

  return OTPTriggerResponse(success=True)


@router.post("/initiate/sms")
async def initiate_otp_request(request: OTPTriggerSMSRequest, 
  Authorize: AuthJWT = Depends(),
  session: AsyncSession = Depends(get_async_session)):
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
  initiate_otp_via_sms.apply_async(args=[user.id])

  return OTPTriggerResponse(success=True)

@router.post("/verify")
async def verify_otp(request: OTPVerifyRequest, 
  Authorize: AuthJWT = Depends(),
  session: AsyncSession = Depends(get_async_session)):
  """ Attempt to authenticate a user and issue JWT token
  
  """
  pass