from sqlalchemy.ext.asyncio import AsyncSession
from taskiq_dependencies import Depends

from ...db import get_async_session
from ...email import sender
from ...broker import broker
from ...settings import settings

from ...models import User


@broker.task
async def send_reset_password_email(
    user_id: str,
    session: AsyncSession = Depends(get_async_session)
) -> None:
    user = await User.get(session, user_id)

    # Create a verification code, this is available
    # only at the time of calling this
    reset_password_token = await user.get_verification_token(session)

    sender.send(
        receivers=[user.email],
        subject="Your verification email",
        text_template="email_reset_password_token.txt",
        html_template="email_reset_password_token.html",
        body_params={
            "domain": "google.com",
            "password_reset_code": reset_password_token,
            "user": user,
        },
    )


@broker.task
async def send_account_verification_email(
    user_id: str,
    session: AsyncSession = Depends(get_async_session)
) -> None:

    user = await User.get(session, user_id)

    # Create a verification code, this is available
    # only at the time of calling this
    verification_token = await user.get_verification_token(session)

    sender.send(
        receivers=[user.email],
        subject="Your verification email",
        text_template="email_verify_account.txt",
        html_template="email_verify_account.html",
        body_params={
            "domain": "google.com",
            "verification_code": verification_token,
            "user": user,
        },
    )


@broker.task
async def send_welcome_email(
    user_id: str,
    session: AsyncSession = Depends(get_async_session)
) -> None:
    user = await User.get(session, user_id)


@broker.task
async def send_otp_sms(
    user_id: str,
    session: AsyncSession = Depends(get_async_session)
) -> None:
    user = await User.get(session, user_id)


@broker.task
async def send_otp_email(
    user_id: str,
    session: AsyncSession = Depends(get_async_session)
) -> None:
    """
    Generates the OTP for a user and email it to them

    This is almost identical to the send_otp_sms task
    except that it sends the OTP via email instead of SMS.
    """
    user = await User.get(session, user_id)

    otp = user.get_otp(
        digits=settings.verbosity.totp_length,
        timeout=settings.lifetime.totp_token,
    )

    sender.send(
        receivers=[user.email],
        subject="Your one time password",
        text_template="email_otp.txt",
        html_template="email_otp.html",
        body_params={
            "otp": otp,
            "user": user,
        },
    )
