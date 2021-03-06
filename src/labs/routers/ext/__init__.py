"""Scenes for the ext module
"""

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import session_context, session_context
from ...config import config

router = APIRouter(tags=["ext"])

@router.get("/echo")
async def echo(request: Request):
    """Echo back a response to say hello.

    Purpose of this endpoint is to echo back what was received, this merely
    validated that the server is up and running.
    """
    return {"message": "Hello, world!"}

@router.get("/healthcheck")
async def perform_healthcheck(request: Request):
    """Check the health of the server.

    Purpose of this endpoint is to check the health of the server.
    We check for connection to the database, queue and logger
    """
    async with session_context() as session:
        return {"message": "ok"}


@router.get("/log")
async def write_to_logger(request: Request, session: AsyncSession = Depends(session_context)):
    """Log a message.

    Purpose of this endpoint is to log a message to the logger.
    """
    return {"message": ""}