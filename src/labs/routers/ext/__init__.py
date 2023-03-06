"""Scenes for the ext module
"""

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_async_session
from ...schema import HealthCheckResponse

router = APIRouter(tags=["ext"])

@router.get("/echo")
async def echo():
    """Echo back a response to say hello.

    Purpose of this endpoint is to echo back what was received, this merely
    validated that the server is up and running.
    """
    return {"message": "Hello, world!"}

@router.get(
    "/healthcheck",
)
async def get_health(
    session: AsyncSession = Depends(get_async_session)
) -> HealthCheckResponse:
    """Check the health of the server.

    Purpose of this endpoint is to check the health of the server.
    We check for connection to the database, queue and logger
    """
    response = HealthCheckResponse()
    response.db_ok = session.is_active
    

    return response

@router.get("/log")
async def test_logger(
    session: AsyncSession = Depends(get_async_session)
):
    """Log a message.

    Purpose of this endpoint is to log a message to the logger.
    """
    return {"message": ""}