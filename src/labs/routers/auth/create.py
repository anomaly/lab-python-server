""" Verification submodule

 This is a submodule that contains API endpoint

"""

from fastapi import APIRouter, Depends,\
  HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_async_session
from ...models.user import User
from ...schema.auth import SignupRequest, SignupResponse,\
  VerifyAccountRequest

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
    raise HTTPException(
       status_code=status.HTTP_400_BAD_REQUEST, 
       detail="User already exists"
    )

  user = await User.create(session, **request.dict())

  # We should have a user here, otherwise something went wrong
  if not user:
    raise HTTPException(
       status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
       detail="Unable to create user"
    )

  # Queue a task to send the verification email
  await send_account_verification_email.kiq(user.id)

  return SignupResponse(
    success=True,
    email=user.email
  )


@router.post("/verify")
async def verify_user(
  request: VerifyAccountRequest,
  session: AsyncSession = Depends(get_async_session),
):
    """Verify an account
    """
    return {"message": "hello world"}