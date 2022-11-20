""" Authentication and Crypto abstractions

This module provides a set of utilities to help with authentication and
crypto related tasks. The output of the various functions are meant to be
stored in databases or used for generating authenticated sessions.

The aim is to abstract these away from the models or routers, so that
they can be used in a variety of contexts.

These are also heavily inspired by the FastAPI documentation:
https://fastapi.tiangolo.com/tutorial/security/

"""

from passlib.context import CryptContext

# Password hashing and validation helpers

# The following should not be called directly
_pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def verify_password(
    plain_password,
    hashed_password
) -> bool:
    """ Use the crypt context to verify the password
    """
    return _pwd_context.verify(
        plain_password,
        hashed_password
    )

def hash_password(password) -> str:
    """ Use the crypt context to hash the password

    This is used by the setter in the User model to hash
    the password when the handlers set the property.
    """
    return _pwd_context.hash(password)

