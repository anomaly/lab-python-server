"""An application user
"""

from sqlalchemy import JSON, Boolean, Column, ForeignKey, String
from sqlalchemy.sql import expression

from ..db import Base
from .utils import DateTimeMixin, IdentifierMixin

class User(Base, IdentifierMixin, DateTimeMixin):
    """
    """
    
    __tablename__ = "user"

    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    verified = Column(Boolean, server_default=expression.false(), nullable=False)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    admin = Column(Boolean, server_default=expression.false(), nullable=False)

