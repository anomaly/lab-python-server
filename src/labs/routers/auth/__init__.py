""" Authentication related handler

  Common handlers for authentication, which is sub-divided to
  modules, each one of them has a router which will be imported
  and mounted onto the router that the package.

"""
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Request, Depends,\
  HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession


from ...db import get_async_session
from ...models import User
from ...schema import UserResponse, Token
from ...utils.auth import create_access_token
from ..utils import get_current_user

from .create import router as router_account_create
from .otp import router as router_otp
 
"""Mounts all the sub routers for the authentication module"""
router = APIRouter(tags=["auth"])

router.include_router(router_account_create)
router.include_router(router_otp, prefix="/otp")

@router.post(
  "/token",
  summary="Provides an endpoint for login via email and password",
)
async def login_for_auth_token(
  form_data: OAuth2PasswordRequestForm = Depends(),
  session: AsyncSession = Depends(get_async_session)
) -> Token:
  """ Attempt to authenticate a user and issue JWT token
  
  """
  user = await User.get_by_email(
    session,
    form_data.username
  )

  if user is None or not user.check_password(form_data.password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Bearer"},
    )

  access_token = create_access_token(
    subject=user.id,
    fresh=True
  )
  
  return Token(
    access_token=access_token,
    token_type="bearer"
  )

@router.post(
  "/refresh",
  summary=""" Provides an endpoint for refreshing the JWT token""",
)
async def refresh_jwt_token(request: Request,
  session: AsyncSession = Depends(get_async_session)
) -> Token:
  """ Provides a refresh token for the JWT session.
  """
  return {}


@router.post(
  "/logout",
  summary=""" Provides an endpoint for logging out the user""",
)
async def logout_user(
  session: AsyncSession = Depends(get_async_session)
):
  """ Ends a users session
  
  """
  return {}

@router.get(
  "/me",
)
async def get_me(
  current_user: User = Depends(get_current_user)
) -> UserResponse:
  """Get the currently logged in user or myself

  This endpoint will return the currently logged in user or raise
  and exception if the user is not logged in.
  """
  return current_user

