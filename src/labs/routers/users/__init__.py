""" User related routes to manage accounts

This should only be accessible to admin users, and are endpoints
used to manage user accounts. For the template application this
was built to test out the initial CRUD features.
"""
from datetime import datetime
from uuid import UUID
from typing import List

from fastapi import APIRouter, Request, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...db import get_async_session
from ...models import User
from ...schema import UserResponse

router = APIRouter(tags=["user"])

@router.get(
    "", 
    summary="Query users between limits",
    response_model=List[UserResponse]
)
async def get_users_with_limits(
    offset: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session)
):
    users = await User.get_all_in_range(
        session,
        offset=skip,
        limit=limit
    )
    return users

@router.get(
    "/infinite", 
    summary="Get all users"
)
async def get_users(
    next_id: UUID = None,
    limit: int = 10,
    session: AsyncSession = Depends(get_async_session)
):
    pass



@router.get(
    "/{id}", 
    summary="Get a particular user"
)
async def get_user_by_id(
    id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    pass

@router.delete(
    "/{id}", 
    summary="Delete a particular user"
)
async def delete_user(
    id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    pass

@router.patch(
    "/{id}", 
    summary="Update a particular user"
)
async def update_user(
    id: UUID,
    session: AsyncSession = Depends(get_async_session)
):
    pass


@router.post(
    "", 
    summary="Create a new user"
)
async def create_user(
    session: AsyncSession = Depends(get_async_session)
):
    pass
