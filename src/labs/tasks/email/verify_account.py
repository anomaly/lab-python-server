"""Send verification email
"""

from labs.celery import app

@app.task(name="VerifyEmail")
def task():
    import logging
    logging.info("Hell world")