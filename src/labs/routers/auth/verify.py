""" Verification submodule

 This is a submodule that contains API endpoint

"""

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import session_context, session_context
from ...config import config

router = APIRouter()

@router.get("/verify")
async def log(request: Request):
    """Verify an account
    """
    return {"message": "hello world"}