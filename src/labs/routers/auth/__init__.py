""" Authentication related handler

  Common handlers for authentication, which is sub-divided to
  modules, each one of them has a router which will be imported
  and mounted onto the router that the package.

"""
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession


from ...db import session_context, get_async_session
from ...models import User
from ...schema import UserRequest,\
  PasswordLoginRequest, AuthResponse

from .create import router as router_account_create
from .otp import router as router_otp
 
"""Mounts all the sub routers for the authentication module"""
router = APIRouter(tags=["auth"])

router.include_router(router_account_create)
router.include_router(router_otp, prefix="/otp")

@router.post("/login",
  summary=""" Provides an endpoint for login via email and password
  """,
  response_model=AuthResponse,
  operation_id="login_user",
)
async def login_user(request: PasswordLoginRequest, 
  Authorize: AuthJWT = Depends(),
  session: AsyncSession = Depends(get_async_session)):
  """ Attempt to authenticate a user and issue JWT token
  
  """
  user = await User.get_by_email(session, request.username)

  if user is None:
    raise HTTPException(status_code=401, detail="Failed to authenticate user")

  access_token = Authorize.create_access_token(subject=user.email,fresh=True)
  refresh_token = Authorize.create_refresh_token(subject=user.email)

  return AuthResponse(access_token=access_token,
                      refresh_token=refresh_token,
                      token_type="Bearer",
                      expires_in=100)

@router.post("/refresh",
  summary=""" Provides an endpoint for refreshing the JWT token""",
  response_model=AuthResponse,
  operation_id="refresh_token",
)
async def refresh_jwt_token(request: Request,
  Authorize: AuthJWT = Depends(),
  session: AsyncSession = Depends(session_context)):
  """ Provides a refresh token for the JWT session.
  """
  Authorize.jwt_refresh_token_required()

  current_user = Authorize.get_jwt_subject()
  new_access_token = Authorize\
    .create_access_token(subject=current_user,
    fresh=False)
  return {}


@router.post("/logout",
  summary=""" Provides an endpoint for logging out the user""",
  operation_id="logout_user"
)
async def logout_user(session: AsyncSession = Depends(session_context)):
  return {}

@router.get("/me", response_model=UserRequest)
async def get_me(request: Request,
  Authorize: AuthJWT = Depends(),
  session: AsyncSession = Depends(session_context)):
  """Get the currently logged in user or myself

  This endpoint will return the currently logged in user or raise
  and exception if the user is not logged in.
  """
  Authorize.jwt_required()
  model = UserRequest(
    id = UUID('{12345678-1234-5678-1234-567812345678}'),
    first_name="Dev",
    last_name="Mukherjee",
    email="hello@anomaly.ltd",
    mobile_phone="042-1234567",
    verified=True,
    created_at=datetime.now(),
    updated_at=datetime.now()
  )
  
  return model

