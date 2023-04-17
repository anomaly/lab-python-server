from datetime import datetime

from pydantic import BaseModel, validator

class HealthCheckResponse(BaseModel):
    """ Provides a health check response with a timestamp

    All cloud native applications should provide a health check endpoint
    for loadbalancers to see if the application is healthy
    """

    all_ok: bool = False
    db_ok: bool = False
    queue_ok: bool = False
    log_ok: bool = False
    timestamp: datetime = datetime.now()
