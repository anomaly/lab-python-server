"""An application user
"""

from sqlalchemy import JSON, Boolean, Column, ForeignKey, String
from sqlalchemy.sql import expression
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from ..db import Base
from .utils import DateTimeMixin, IdentifierMixin, ModelCRUDMixin

class User(Base, IdentifierMixin, DateTimeMixin, ModelCRUDMixin):
    """
    """
    
    __tablename__ = "user"

    email = Column(String,
        unique=True,
        nullable=True)

    hashed_password = Column(String,
        nullable=True)

    verified = Column(Boolean,
        server_default=expression.false(), 
        nullable=False)

    mobile_number = Column(String,
        nullable=True)

    first_name = Column(String,
        nullable=True)

    last_name = Column(String,
        nullable=True)

    is_admin = Column(Boolean, 
        server_default=expression.false(), 
        nullable=False)

    otp_secret = Column(String,
        nullable=True)

    @classmethod
    async def get_by_email(cls, session, email):
        query = select(cls).where(cls.email == email)
        try:
            results = await session.execute(query)
            (result,) = results.one()
            return result
        except NoResultFound: # noqa: E722
            return None

    @classmethod
    async def get_by_phone(cls, session, phone):
        query = select(cls).where(cls.mobile_number == phone)
        try:
            results = await session.execute(query)
            (result,) = results.one()
            return result
        except NoResultFound: # noqa: E722
            return None
