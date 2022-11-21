from datetime import datetime

from pydantic import BaseModel, validator

class HealthCheckResponse(BaseModel):

    all_ok: bool = False
    db_ok: bool = False
    queue_ok: bool = False
    log_ok: bool = False
    timestamp: datetime = datetime.now()
