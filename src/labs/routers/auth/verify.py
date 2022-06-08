"""Scenes for the ext module
"""

from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ....db import session_context, session_context
from . import router


@router.get("/verify")
async def log(request: Request, session: AsyncSession = Depends(session_context)):
    """Verify an account
    """
    return {"message": "hello world"}