""" An application user

 The aim is to provide a set of fields that are common to most
 applications with a good know set of practices around authentication
 both via password and one time passwords.

"""

from typing import Optional
from datetime import datetime

from sqlalchemy import event
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Mapped, mapped_column

# OTP helpers from pyotp
from pyotp import TOTP, random_base32

from ..db import Base
from ..config import config
from .utils import DateTimeMixin, IdentifierMixin,\
    ModelCRUDMixin
    
from ..utils.auth import hash_password, verify_password

class User(
    Base,
    IdentifierMixin,
    DateTimeMixin,
    ModelCRUDMixin
):
    """
    A user defines a person that will use various software systems

    Users have authentication built into the system with support
    for password based auth and one time passwords.
    """
    
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(unique=True)
    mobile_number: Mapped[Optional[str]]
    
    """
    Note that we define the password slightly differently

        The Column knows to provision the field as password
        however we will override the getter and more importantly
        the setter. The setter will hash the password whenever
        the user wishes to update this. 

        This will make the code on the API side cleaner and will
        ensure that the password is never stored in plain text.

    """
    password: Mapped[str]
    otp_secret: Mapped[str]

    verification_token: Mapped[Optional[str]]
    verification_token_expiry: Mapped[Optional[datetime]]

    first_name: Mapped[str]
    last_name: Mapped[str]

    is_admin: Mapped[bool] = mapped_column(
        default=False,
    )

    verified: Mapped[bool] = mapped_column(
        default=False,
    )

    # Methods to assist to deal with passwords
    def check_password(self, plain_text_pass):
        return verify_password(plain_text_pass, self.password)
    
    def get_verification_code(
        self,
    ) -> str:
        """
        Generates a new verification code and updates the object and returns the
        plain string code.

            Returns:
                verification_code (str): The verification code
        """
        # Generate a random secret
        verification_code = random_base32()

        # Verification code is hashed and only sent back
        # to the user via email or SMS, this should not be resent
        # and you should initiate a new verification code if the
        # user is unable to access the code sent to them 
        self.__class__.update(
            self.session,
            verification_code = hash_password(verification_code),

        )

        return verification_code

    def get_otp(
        self, 
        digits: int = 6, 
        timeout: int = 30
    ):
        """ Get the current OTP for the user

        This is sent to the user via email or SMS and is used to
        authenticate the user. This should be different based
        on the timeout and the digits.
        """
        otp = TOTP(self.secret, digits=digits, interval=timeout)
        return otp.now()
    
    def verify_otp(
            self, 
            token: str,
            timeout: int = 30, 
            window: int = 30
        ):
        """
        """
        otp = TOTP(self.secret, interval=timeout)
        return otp.verify(token, valid_window=window)
    
    def get_verification_token(self):
        """ Get the verification token for the user

        This is used to verify the user's account
        """
        return self.get_otp()

    @classmethod
    async def get_by_email(cls, session, email):
        """ A custom getter where the user is found via email 

        The aim is to assist with finding the user by email
        which is handy when authenticating via passwords
        """
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

def encrypt_password(target, value, oldvalue, initiator):
    """ Encrypt the password when it is set

    This enables the application logic to simply set the plain
    text password and the model encrypts it on the way in.

    The idea is to abstract this from the duties of the application.
    """
    return hash_password(value)

# Support for the above method to run when the password is set
event.listen(
    User.password, 
    'set', 
    encrypt_password, 
    retval=True
)

