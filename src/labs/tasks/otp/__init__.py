""" OTP related tasks 

"""
# App related imports

from ..utils import send_sms_message, email_sender
from ...db import get_async_session
from ...models import User

async def initiate_otp_via_sms(user_id):

    session = get_async_session()
    user = await User.get(session, user_id)

    import logging
    logging.error(user)
    
    #async_to_sync(get_user_info)(user_id)
    #send_sms_message("00000", "Your OTP is 1234")


async def initiate_otp_via_email(user_id):
    email_sender.send(
        subject='email subject',
        sender="",
        receivers=[],
        text="Hi, this is an email."
    )