""" Shared resources for routing messages 
"""

from redmail import EmailSender
import clicksend_client 

from ..config import config

# Email sender via SMTP server
email_sender = EmailSender(
    host=config.SMTP_HOST,
    port=config.SMTP_PORT,
    username=config.SMTP_USER,
    password=config.SMTP_PASSWORD,
    use_starttls=False,
    )

def send_sms_message(phone_number: str, message: str):
    """ Warpper to send SMS messages

    The default implementation is specific to ClickSend SMS API.
    This wrapper ensures that we can override the implementaiton 
    per use case.

    """

    # Configuration required by clicksend_client
    _cs_config = clicksend_client.Configuration()
    _cs_config.username = config.SMS_API_KEY
    _cs_config.password = config.SMS_API_SECRET

    # Clicksend overarching client
    sms_client = clicksend_client\
        .SMSApi(clicksend_client.ApiClient(_cs_config))

    sms_message = clicksend_client.SmsMessage(
        _from="ANOMALY",
        body=message,
        to=phone_number,
    )

    sms_messages = clicksend_client.SmsMessageCollection(
        messages=[sms_message]
        )

    try:
        response = sms_client.sms_send_post(sms_messages)
        return True
    except ApiException as e:
        import logging
        logging.error("Exception when calling SMSApi->sms_send_post: %s\n" % e)
        return False
    

