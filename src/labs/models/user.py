"""An application user
"""

from sqlalchemy import JSON, Boolean, Column, ForeignKey, String
from sqlalchemy.sql import expression
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from ..db import Base
from .utils import DateTimeMixin, IdentifierMixin

class User(Base, IdentifierMixin, DateTimeMixin):
    """
    """
    
    __tablename__ = "user"

    email = Column(String,
        unique=True,
        nullable=False)

    hashed_password = Column(String,
        nullable=False)

    verified = Column(Boolean,
        server_default=expression.false(), 
        nullable=False)

    first_name = Column(String,
        nullable=False)

    last_name = Column(String,
        nullable=False)

    is_admin = Column(Boolean, 
        server_default=expression.false(), 
        nullable=False)

    @classmethod
    async def get_by_email(cls, session, email):
        query = select(cls).where(cls.email == email)
        try:
            results = await session.execute(query)
            (result,) = results.one()
            return result
        except NoResultFound: # noqa: E722
            return None
