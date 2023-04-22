""" Verification submodule

 This is a submodule that contains API endpoint

"""

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_async_session
from ...models import User
from ...schema import SignupRequest
from ...config import config

from .tasks import send_account_verification_email

router = APIRouter()

@router.post("/signup")
async def signup_user(request: SignupRequest, 
  session: AsyncSession = Depends(get_async_session)
):
  # Try and get a user by email
  user = await User.get_by_email(session, request.email)
  if user:
    raise HTTPException(status_code=400, detail="User already exists")

  await User.create(session, **request.dict())

  return {}


@router.get("/verify")
async def verify_user(request: Request):
    """Verify an account
    """
    await send_account_verification_email.kiq()
    return {"message": "hello world"}