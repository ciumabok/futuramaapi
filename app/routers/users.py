from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import Annotated

from app.repositories.sessions import get_async_session
from app.services.auth import oauth2_scheme
from app.services.security import AccessTokenData
from app.services.users import (
    User,
    UserAdd,
    UserUpdate,
    process_activate,
    process_add_user,
    process_get_me,
    process_update,
)

router = APIRouter(prefix="/users")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
    name="user",
)
async def add_user(
    body: UserAdd,
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """Create User.

    The user add endpoint is an API function allowing the creation of new user accounts.
    It receives user details via HTTP requests, validates the information,
    and stores it in the system's database.
    This endpoint is essential for user registration and onboarding.

    Please note that currently endpoint is not protected.
    However, if there are a lot of spam requests, the endpoint will be blocked or limited.
    """
    return await process_add_user(body, session)


@router.get(
    "/me",
    response_model=User,
    name="user_me",
)
async def get_me(
    token: Annotated[AccessTokenData, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """Get user details.

    Retrieve authenticated user profile information, including username, email, and account details.
    Personalize user experiences within the application using the JSON response containing user-specific data.
    """
    return await process_get_me(token, session)


@router.get(
    "/activate",
    response_model=User,
    name="activate_user",
)
async def activate(
    sig: str,
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """Get user details.

    Retrieve authenticated user profile information, including username, email, and account details.
    Personalize user experiences within the application using the JSON response containing user-specific data.
    """
    return await process_activate(sig, session)


@router.put(
    "/",
    response_model=User,
    name="update_user",
)
async def update(
    user: UserUpdate,
    token: Annotated[AccessTokenData, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """Update user details.

    This endpoint is crucial for users to manage and maintain accurate profile information,
    often including authentication and authorization checks for security.
    """
    return await process_update(token, user, session)
