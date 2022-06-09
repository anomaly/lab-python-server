"""Send verification email
"""

from labs.celery import app

@app.task(ignore_result=True)
def email():
    import logging
    logging.info("Hell world")