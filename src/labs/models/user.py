""" An application user

 The aim is to provide a set of fields that are common to most
 applications with a good know set of practices around authentication
 both via password and one time passwords.

"""

from typing import Optional
from datetime import datetime, timedelta
from secrets import token_urlsafe

from sqlalchemy import event
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_object_session

# OTP helpers from pyotp
from pyotp import TOTP

from ..db import Base
from ..settings  import settings
from .utils import DateTimeMixin, IdentifierMixin,\
    ModelCRUDMixin, timestamp
 
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

    # Used to store a temporary token to verify the user
    verification_token: Mapped[Optional[str]]
    verification_token_expiry: Mapped[Optional[timestamp]]

    # Used to store a temporary token to reset the password
    reset_token: Mapped[Optional[str]]
    reset_token_expiry: Mapped[Optional[timestamp]]

    # Basic user information
    first_name: Mapped[str]
    last_name: Mapped[str]

    # Used to indicate if the user is an admin
    is_admin: Mapped[bool] = mapped_column(
        default=False,
    )

    # Set by the verification endpoint to indicate that the user
    # was able to get through the verification process
    verified: Mapped[bool] = mapped_column(
        default=False,
    )

    # Methods to assist to deal with passwords
    def check_password(self, plain_text_pass):
        return verify_password(plain_text_pass, self.password)
    
    async def verify_user_account(
        self,
        async_object_session,
        verification_token: str,
    ) -> bool:
        """
        Verifies the user account using the verification token
        """

        # No verification token or expiry date found, so there's
        # no point in going any further
        if not self.verification_token or not self.verification_token_expiry:
            return False
        
        # The expiry token is invalid, so we should clean up the token
        # and return a false, this is so the token can't be retried
        if self.verification_token_expiry < datetime.utcnow():
            self.verification_token = None
            self.verification_token_expiry = None

            async_object_session.add(self)
            await async_object_session.commit()

            return False
        
        # The token failed to match, so we should return a false
        if not verify_password(verification_token, self.verification_token):
            return False
        
        # All has gone well, we can make the user active and clear
        # the token so it can't be used again

        self.verification_token = None
        self.verification_token_expiry = None

        self.verified = True
        
        async_object_session.add(self)
        await async_object_session.commit()

        return True

    async def get_verification_token(
        self,
        async_object_session,
    ) -> str:
        """
        Generates a new verification code and updates the object and returns the
        plain string code.

            Returns:
                verification_code (str): The verification code
        """
        # Generate a random secret
        verification_code = token_urlsafe(
            settings.verbosity.verification_token
        )

        verification_token_expiry = datetime.utcnow() + \
            timedelta(seconds=settings.lifetime.token_account_verification)

        # Verification code is hashed and only sent back
        # to the user via email or SMS, this should not be resent
        # and you should initiate a new verification code if the
        # user is unable to access the code sent to them
        self.verification_token = hash_password(verification_code)
        self.verification_token_expiry = verification_token_expiry

        async_object_session.add(self)
        await async_object_session.commit()

        return verification_code
    
    async def reset_password(
        self,
        async_object_session,
        reset_token: str,
        new_password: str,
    ) -> bool:
        """
        Attempt to verify the reset password token and update the password


        """
        if not self.reset_password or not self.reset_password_expiry:
            return False
        
        if self.reset_password_expiry < datetime.utcnow():
            self.reset_password = None
            self.reset_password_expiry = None

            async_object_session.add(self)
            await async_object_session.commit()

            return False
        
        if not verify_password(reset_token, self.reset_password):
            return False
        
        self.reset_password = None
        self.reset_password_expiry = None

        self.password = hash_password(new_password)

        async_object_session.add(self)
        await async_object_session.commit()

        return True

    async def get_reset_password_token(
        self,
        async_object_session,
    ) -> str:
        """
        Generates a new reset password code and updates the object 
        and returns the plain string code.

            Returns:
                reset_password_token (str): The verification code
        """
        # Generate a random secret
        reset_password_token = token_urlsafe(
            settings.verbosity.reset_password_token
        )

        reset_password_token_expiry = datetime.utcnow() + \
            timedelta(seconds=settings.lifetime.token_reset_password)

        # Password reset token is hashed and only sent back
        # to the user via email or SMS, this should not be resent
        # and you should initiate a new verification code if the
        # user is unable to access the code sent to them
        self.reset_token = hash_password(reset_password_token)
        self.reset_token_expiry = reset_password_token_expiry

        async_object_session.add(self)
        await async_object_session.commit()

        return reset_password_token


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
        otp = TOTP(
            self.otp_secret, 
            digits=digits, 
            interval=timeout
        )  
        
        return otp.now()
    
    def verify_otp(
            self, 
            token: str,
            timeout: int = 30, 
            window: int = 30
        ) -> bool:
        """
        Verifies if the sent OTP is valid for the user
        """
        otp = TOTP(self.otp_secret, interval=timeout)
        return otp.verify(token, valid_window=window)
    
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
