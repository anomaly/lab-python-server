"""Database models described using SQLAlchemy.

"""

from sqlalchemy import Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from .user import User

Base = declarative_base()

class IdentifierMixin(object):
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        nullable=False,
    )
class DateTimeMixin(object):
    created_at = Column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=text("now()"),
        onupdate=text("now()"),
        nullable=False,
    )
