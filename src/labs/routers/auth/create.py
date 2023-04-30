""" Verification submodule

 This is a submodule that contains API endpoint

"""

from fastapi import APIRouter, Request, Depends,\
  HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_async_session
from ...models.user import User
from ...schema.auth import SignupRequest, SignupResponse

from .tasks import send_account_verification_email

router = APIRouter()

@router.post(
    "/signup",
      status_code = status.HTTP_201_CREATED,
)
async def signup_user(
   request: SignupRequest, 
   session: AsyncSession = Depends(get_async_session)
) -> SignupResponse:
  """ Sign up the user using email and password

  The general sign up for uses a email, password and first
  and last names to create a user. The handler will check
  to see if the user already exists and if not, create the
  user and return a success response.
  """

  # Try and get a user by email
  user = await User.get_by_email(session, request.email)
  if user:
    raise HTTPException(status_code=400, detail="User already exists")

  await User.create(session, **request.dict())

  return SignupResponse(
    success=True,
    email=request.email
  )


@router.get("/verify")
async def verify_user(request: Request):
    """Verify an account
    """
    await send_account_verification_email.kiq()
    return {"message": "hello world"}