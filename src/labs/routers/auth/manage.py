
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_async_session
from ...models.user import User
from ...dto.auth import ResetPasswordRequest

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
