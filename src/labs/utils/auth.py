""" Authentication and Crypto abstractions

This module provides a set of utilities to help with authentication and
crypto related tasks. The output of the various functions are meant to be
stored in databases or used for generating authenticated sessions.

The aim is to abstract these away from the models or routers, so that
they can be used in a variety of contexts.

These are also heavily inspired by the FastAPI documentation:
https://fastapi.tiangolo.com/tutorial/security/

"""

from datetime import datetime, timedelta

import bcrypt
import jwt

from ..settings  import settings

def verify_password(
    plain_password,
    hashed_password
) -> bool:
    """ Use the crypt context to verify the password

    the str.encode is used to convert the string to bytes
    """
    return bcrypt.checkpw(
        str.encode(plain_password),
        str.encode(hashed_password)
    )

def hash_password(password) -> str:
    """ Use the crypt context to hash the password

    This is used by the setter in the User model to hash
    the password when the handlers set the property.

    the input string has to be an byte string
    """
    encoded_password = bcrypt.hashpw(
        str.encode(password),
        bcrypt.gensalt()
    )
    # Return a string representation so that it can be stored
    return encoded_password.decode()


def create_access_token(
    subject: str,
    fresh: bool = False
) -> str:
    """ Creates a JWT token for the user

    This is used by the authentication handler to create
    a JWT token for the user to use for subsequent requests.

    Args:
        subject (str): The subject of the token, usually the email
        expires_delta (int, optional): The number of seconds the token
            should be valid for. Defaults to None.
        fresh (bool, optional): Whether the token is fresh or not.
            Defaults to False.

    Returns:
        str: The encoded JWT token
    """
    delta = timedelta(seconds=settings.lifetime.token_jwt_access)
    to_encode = {
        "sub": subject,
        "fresh": fresh,
        "exp": datetime.utcnow() + delta
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY.get_secret_value(),
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt
