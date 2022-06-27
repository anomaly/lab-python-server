
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, NoneStr
from pydantic.uuid import UUID

class User(BaseModel):
    id: UUID
    