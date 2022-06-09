""" Authentication related handler

  Common handlers for authentication, which is sub-divided to
  modules, each one of them has a router which will be imported
  and mounted onto the router that the package.

"""
from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import session_context, session_context
from ...models import User
from .verify import router as router_verify
 
"""Mounts all the sub routers for the authentication module"""
router = APIRouter(tags=["auth"])

router.include_router(router_verify)

@router.get("/me")
async def get_me(session: AsyncSession = Depends(session_context)):
  return {}


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
