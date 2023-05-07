
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_async_session
from ...models.user import User
from ...schema.auth import InitiateResetPasswordRequest, ResetPasswordRequest

from .tasks import send_reset_password_email

router = APIRouter()

@router.post(
    "/reset",
)
async def reset_password(
    request: ResetPasswordRequest,
    session: AsyncSession = Depends(get_async_session),   
):
    user = await User.get_by_email(
       session, 
       request.email
    )

     # Even if there's an error we aren't going to reveal the
     # fact that the user exists or not
    if not user:
      raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
      )
    
    reset_password_outcome = await user.reset_password(
        session,
        request.reset_token,
        request.password
    )

    if not reset_password_outcome:
      raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Reset password failed" 
      )


@router.post(
    "/initiate/reset",
    status_code=status.HTTP_202_ACCEPTED
)
async def initiate_password_reset(
    request: InitiateResetPasswordRequest,
    session: AsyncSession = Depends(get_async_session),
):
    user = await User.get_by_email(
       session, 
       request.email
    )

     # Even if there's an error we aren't going to reveal the
     # fact that the user exists or not
    if not user:
      raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
      )
    
    reset_password_token = await user.get_reset_password_token(
      session, 
      request.email
    )

    if not reset_password_token:
      raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Initiate reset password failed" 
      )
    
    # Queue a task to send the verification email
    await send_reset_password_email.kiq(user.id)
