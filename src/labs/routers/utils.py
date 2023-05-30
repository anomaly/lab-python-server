""" Utility functions for routers

    A set of utility function to assist with authentication,
    authorization and other dependencies that routers and
    endpoints can use.

"""

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from ..settings  import settings
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
      settings.jwt.secret_key.get_secret_value(),
      algorithms=[settings.jwt.algorithm]
    )

    user_id: str = payload.get("sub")

    if user_id is None:
        raise credentials_exception

    token_data = TokenData(id=user_id)

  except:
    raise credentials_exception

  user = await User.get(session, token_data.id)

  if user is None:
      raise credentials_exception

  return user


async def get_admin_user(
  current_user: User = Depends(get_current_user)
):
  """ Demonstrates wrapping the base Dependency to a more specific one

  You would use the same pattern to make sure that the user is
  an administrator or other specific roles.

  Note: see the use of OAuth2 scopes for this purpose. 

  """
  if not current_user.is_admin:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Inactive user"
    )
  return current_user