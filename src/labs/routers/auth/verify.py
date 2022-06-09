""" Verification submodule

 This is a submodule that contains API endpoint

"""

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import session_context, session_context
from ...tasks.email import verification_email
from ...config import config

router = APIRouter()

@router.get("/verify")
async def verify_user_account(request: Request):
    """Verify an account
    """
    verification_email.delay()
    return {"message": "hello world"}