from datetime import datetime

from pydantic import BaseModel


class EchoResponse(BaseModel):
    """ A simple echo response """
    message: str

class HealthCheckResponse(BaseModel):
    """ Provides a health check response with a timestamp

    All cloud native applications should provide a health check endpoint
    for loadbalancers to see if the application is healthy
    """

    all_ok: bool = False
    db_ok: bool = False
    queue_ok: bool = False
    timestamp: datetime = datetime.now()

class RootResponse(BaseModel):
    """ Response sent by the root endpoint

    Used to echo back the request and tell the client that
    the API is ready and available to the world
    """
    root_path: str
    message: str