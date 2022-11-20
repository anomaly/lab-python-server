"""An application user
"""

from sqlalchemy import Boolean, Column, String, event
from sqlalchemy.sql import expression
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

# OTP helpers from pyotp
from pyotp import TOTP, random_base32

from ..db import Base
from .utils import DateTimeMixin, IdentifierMixin,\
    ModelCRUDMixin

from ..utils.auth import hash_password, verify_password

class User(Base, IdentifierMixin, DateTimeMixin, ModelCRUDMixin):
    """ A user defines a person that will use various software systems

    Users have authentication built into the system with support
    for password based auth and one time passwords.
    """
    
    __tablename__ = "user"

    email = Column(String,
        unique=True,
        nullable=True)

    """ Note that we define the password slightly differently

        The Column knows to provision the field as password
        however we will override the getter and more importantly
        the setter. The setter will hash the password whenever
        the user wishes to update this. 

        This will make the code on the API side cleaner and will
        ensure that the password is never stored in plain text.

    """
    _password = Column("password",
        String,
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

    # Password wrapper for hashing when we set 
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        """ Overrides the default setter behaviour to hash the password

            It would be cool to override the comparison method
            if it's simple then we use the equality operator

        """
        self._password = hash_password(password)

    # Methods to assist to deal with passwords
    def check_password(self, plain_text_pass):
        return verify_password(plain_text_pass, self.password)

    def get_otp(self, digits: int, timeout: int):
        """
        """
        otp = TOTP(self.secret, digits=digits, interval=timeout)
        return otp.now()
    
    def verify_otp(self, timeout: int, window: int, token: str):
        otp = TOTP(self.secret, interval=timeout)
        return otp.verify(token, valid_window=window)

    @classmethod
    async def get_by_email(cls, session, email):
        query = cls._base_get_query().where(cls.email == email)
        try:
            results = await session.execute(query)
            (result,) = results.one()
            return result
        except NoResultFound: # noqa: E722
            return None

    @classmethod
    async def get_by_phone(cls, session, phone):
        query = cls._base_get_query().where(
            cls.mobile_number == phone
        )
        try:
            results = await session.execute(query)
            (result,) = results.one()
            return result
        except NoResultFound: # noqa: E722
            return None

    @classmethod
    async def get_by_email_or_mobile(cls, session, email, phone):
        query = cls._base_get_query().where(cls.email == email or\
            cls.mobile_number == phone)
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
    target.otp_secret = random_base32()

