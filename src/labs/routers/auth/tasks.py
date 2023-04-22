from ...broker import broker

@broker.task
async def send_welcome_email() -> None:
    pass

@broker.task
async def send_reset_password_email() -> None:
    pass

@broker.task
async def send_account_verification_email() -> None:
    import logging
    logging.error("Kicking off send_account_verification_email")

@broker.task
async def sent_otp_sms() -> None:
    pass

@broker.task
async def send_otp_email() -> None:
    pass


