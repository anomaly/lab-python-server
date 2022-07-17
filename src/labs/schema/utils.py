"""Shared utilities for pydantic models

"""
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

class IdentityMixin(BaseModel):
    """ Identifier
    """
    id: UUID

class DateTimeMixin(BaseModel):
    """ Adds timestamps to relevant models
    """
    created_at: datetime
    updated_at: datetime
 