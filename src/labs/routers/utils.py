""" Utility functions for routers

    A set of utility function to assist with authentication,
    authorization and other dependencies that routers and
    endpoints can use.

"""

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from ..db import get_async_session

async def get_current_user(session:
  AsyncSession = Depends(get_async_session),
  Authorize: AuthJWT = Depends()
):
  """
  """
  Authorize.jwt_required()
  current_user_email = Authorize.get_jwt_subject()

  user = await User.get_by_email(session, current_user_email)

  if not user:
    raise HTTPException(status_code=404, detail="User not found")

  return user