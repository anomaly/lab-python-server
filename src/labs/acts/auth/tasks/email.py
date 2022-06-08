from ....celery import app

@app.task(name="VerifyEmail")
async def send_welcome_email():
    print("hello world")