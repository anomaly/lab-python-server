"""Email related tasks

"""

from ...celery import app

@app.task(ignore_result=True)
async def verification_email():
    import logging
    logging.info("Hello world")