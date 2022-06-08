"""Scenes for the ext module
"""

from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ....db import session_context, session_context
from ....celery import app as task_queue
from . import router


@router.get("/verify")
async def log(request: Request, session: AsyncSession = Depends(session_context)):
    """Verify an account
    """
    task_queue.send_task("VerifyEmail")
    return {"message": "hello world"}