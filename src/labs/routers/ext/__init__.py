"""Scenes for the ext module
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_async_session
from ...dto.ext import HealthCheckResponse, EchoResponse

router = APIRouter(tags=["ext"])


@router.get("/echo")
async def echo() -> EchoResponse:
    """Echo back a response to say hello.

    Purpose of this endpoint is to echo back what was received, this merely
    validated that the server is up and running.
    """
    return EchoResponse(
        message="Hello World"
    )


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

    # This will be done better with pyndatic 2
    response.all_ok = (
        response.db_ok and
        response.queue_ok and
        response.log_ok
    )

    return response
