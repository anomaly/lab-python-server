"""An application user
"""

from sqlalchemy import Boolean, Column, String, event
from sqlalchemy.sql import expression
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

import pyotp

from ..db import Base
from .utils import DateTimeMixin, IdentifierMixin,\
    ModelCRUDMixin, hash_password
class User(Base, IdentifierMixin, DateTimeMixin, ModelCRUDMixin):
    """
    """
    
    __tablename__ = "user"

    email = Column(String,
        unique=True,
        nullable=True)

    password = Column(String,
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

    async def set_password(self, plain_text_pass):
        pass

    async def check_password(self, plain_text_pass):
        pass

    async def get_otp(self):
        pass

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

@event.listens_for(User, 'init')
def receive_init(target, args, kwargs):
    """ When the user is created, generate a secret for the OTP
    """
    target.otp_secret = pyotp.random_base32()

@event.listens_for(User.password, 'set')
def receive_set(target, value, initiator):
    """ Setting the password will has the value """
    target.password = hash_password(value)