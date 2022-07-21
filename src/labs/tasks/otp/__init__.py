""" OTP related tasks 

"""
import asyncio

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# App related imports
from ...celery import app
from ..utils import send_sms_message, email_sender
from ...db import get_async_session
from ...models import User

async def get_user_info(user_id):
    session = get_async_session()
    user = await User.get(session, user_id)
    return user

@app.task()
def initiate_otp_via_sms(user_id):

    user = loop.run_until_complete(get_user_info(user_id))

    import logging
    logging.error(user)
    
    #async_to_sync(get_user_info)(user_id)
    #send_sms_message("00000", "Your OTP is 1234")


@app.task()
def initiate_otp_via_email(user_id):
    email_sender.send(
        subject='email subject',
        sender="",
        receivers=[],
        text="Hi, this is an email."
    )