""" OTP related tasks 

"""


from ...celery import app

@app.task(ignore_result=True)
def send_otp():
    import logging
    logging.info("Hello world")