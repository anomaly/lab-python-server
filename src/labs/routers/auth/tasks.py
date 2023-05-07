from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends

from ...db import get_async_session
from ...email import sender
from ...broker import broker

from ...models import User

@broker.task
async def send_reset_password_email(
    user_id: UUID,
    session: AsyncSession = TaskiqDepends(get_async_session)
) -> None:
    user = await User.get(session, user_id)

@broker.task
async def send_account_verification_email(
    user_id: UUID,
    session: AsyncSession = TaskiqDepends(get_async_session)
) -> None:

    user = await User.get(session, user_id)

    # Create a verification code, this is available
    # only at the time of calling this 
    verification_code = await user.get_verification_token(session)

    sender.send(
        receivers=[user.email],
        subject="Your verification email",
        text_template="email_verify_account.txt",
        html_template="email_verify_account.html",
        body_params={
            "domain": "google.com",
            "verification_code": verification_code,
            "user": user,
        },
    )

@broker.task
async def send_welcome_email(
    user_id: UUID,
    session: AsyncSession = TaskiqDepends(get_async_session)
) -> None:
    user = await User.get(session, user_id)


@broker.task
async def sent_otp_sms(
    user_id: UUID,
    session: AsyncSession = TaskiqDepends(get_async_session)
) -> None:
    user = await User.get(session, user_id)

@broker.task
async def send_otp_email(
    user_id: UUID,
    session: AsyncSession = TaskiqDepends(get_async_session)
) -> None:
    user = await User.get(session, user_id)


