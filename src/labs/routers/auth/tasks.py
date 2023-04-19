from ...broker import broker

@broker.task
async def send_welcome_email() -> None:
    pass