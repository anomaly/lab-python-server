from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends

from ...db import get_async_session
from ...utils import minio_client
from ...broker import broker


@broker.task
async def verify_s3_file_availability(
    s3_file_metadata_id: str,
    session: AsyncSession = TaskiqDepends(get_async_session)
) -> None:
    pass
