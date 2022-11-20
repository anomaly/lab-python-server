""" Utility functions for routers

    A set of utility function to assist with authentication,
    authorization and other dependencies that routers and
    endpoints can use.

"""

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from ..config import config
from ..db import get_async_session
from ..models import User
from ..schema import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
  token: str = Depends(oauth2_scheme),
  session: AsyncSession = Depends(get_async_session),
):
  """
  """
  # Reused a few times around the lifecycle
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
  )

  try:
    payload = jwt.decode(
      token,
      config.JWT_SECRET_KEY.get_secret_value(),
      algorithms=[config.JWT_ALGORITHM]
    )

    username: str = payload.get("sub")

    if username is None:
        raise credentials_exception

    token_data = TokenData(username=username)

  except:
    raise credentials_exception

  user = await User.get_by_email(session, token_data.username)

  if user is None:
      raise credentials_exception

  return user


async def get_current_active_user(
  current_user: User = Depends(get_current_user)
):
  """ Demonstrates wrapping the base Dependency to a more specific one

  You would use the same pattern to make sure that the user is
  an administrator or other specific roles.

  Note: see the use of OAuth2 scopes for this purpose. 

  """
  if current_user.verified:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Inactive user"
    )
  return current_user