""" OTP related tasks 

"""


from ...celery import app

from ..utils import send_sms_message, email_sender

@app.task()
def initiate_otp_via_sms(user_id):
    send_sms_message("00000", "Your OTP is " + user_id)


@app.task()
def initiate_otp_via_email(user_id):
    email_sender.send(
        subject='email subject',
        sender="",
        receivers=[],
        text="Hi, this is an email."
    )