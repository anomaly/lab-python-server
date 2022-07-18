""" Reference implementation of OTP authentication. 

"""

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import session_context, get_async_session

router = APIRouter(tags=["otp"])

@router.post("/initiate")
async def initiate_otp_request(request: Request, 
  Authorize: AuthJWT = Depends(),
  session: AsyncSession = Depends(get_async_session)):
  """ Attempt to authenticate a user and issue JWT token
  
  """
  pass

@router.post("/verify")
async def verify_otp(request: Request, 
  Authorize: AuthJWT = Depends(),
  session: AsyncSession = Depends(get_async_session)):
  """ Attempt to authenticate a user and issue JWT token
  
  """
  pass