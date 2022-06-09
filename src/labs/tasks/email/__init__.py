"""Email related tasks

"""

from ...celery import app

@app.task(ignore_result=True)
def verification_email():
    import logging
    logging.info("Hello world")