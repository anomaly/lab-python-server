""" Authentication related handler

  Common handlers for authentication, which is sub-divided to
  modules, each one of them has a router which will be imported
  and mounted onto the router that the package.

"""
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from ...db import session_context, session_context
from ...models import User
from ...schema import User as UserSchema
from .verify import router as router_verify
 
"""Mounts all the sub routers for the authentication module"""
router = APIRouter(tags=["auth"])

router.include_router(router_verify)

@router.get("/me", response_model=UserSchema)
async def get_me(session: AsyncSession = Depends(session_context)):
  """Get the currently logged in user or myself

  This endpoint will return the currently logged in user or raise
  and exception if the user is not logged in.
  """

  model = UserSchema(
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


@router.post("/login")
async def login_user(session: AsyncSession = Depends(session_context)):
  """Login a user."""
  return {}


@router.post("/logout")
async def logout_user(session: AsyncSession = Depends(session_context)):
  return {}

@router.post("/signup")
async def signup_user(session: AsyncSession = Depends(session_context)):
  return {}

@router.post("/account")
async def login(session: AsyncSession = Depends(session_context)):
  return {}
