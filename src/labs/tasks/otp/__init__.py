""" OTP related tasks 

"""
import asyncio
from asgiref.sync import async_to_sync

from ...celery import app

from ..utils import send_sms_message, email_sender

async def get_user_info(user_id):
    from ...db import get_async_session
    from ...models import User
    session = get_async_session()
    import logging
    logging.error(session)
    user = await User.get(await session(), user_id)


@app.task()
def initiate_otp_via_sms(user_id):
    #async_to_sync(get_user_info)(user_id)
    send_sms_message("00000", "Your OTP is 1234")


@app.task()
def initiate_otp_via_email(user_id):
    email_sender.send(
        subject='email subject',
        sender="",
        receivers=[],
        text="Hi, this is an email."
    )