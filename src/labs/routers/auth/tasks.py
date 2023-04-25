from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends

from ...db import get_async_session
from ...broker import broker

@broker.task
async def send_welcome_email() -> None:
    pass

@broker.task
async def send_reset_password_email() -> None:
    pass

@broker.task
async def send_account_verification_email(
    session: AsyncSession = TaskiqDepends(get_async_session)
) -> None:
    import logging
    logging.error("Kicking off send_account_verification_email")

@broker.task
async def sent_otp_sms() -> None:
    pass

@broker.task
async def send_otp_email() -> None:
    pass


