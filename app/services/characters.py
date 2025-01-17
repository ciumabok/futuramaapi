from datetime import datetime
from typing import Any, Optional

from fastapi import HTTPException, Request, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_storages import StorageImage
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core import settings
from app.repositories.base import OrderByDirection
from app.repositories.models import Character as CharacterModel
from app.repositories.models import (
    CharacterDoesNotExist,
    CharacterGender,
    CharacterGenderFilter,
    CharacterSpecies,
    CharacterSpeciesFilter,
    CharacterStatus,
    CharacterStatusFilter,
)


def build_url(*, path: str = None):
    path = f"{settings.static}/{path}" if path else f"{settings.static}"
    return HttpUrl.build(
        scheme="https",
        host=settings.trusted_host,
        path=path,
    )


class Character(BaseModel):
    id: int
    name: str
    gender: CharacterGender
    status: CharacterStatus
    species: CharacterSpecies
    created_at: datetime = Field(alias="createdAt")
    image: Optional[HttpUrl]

    @field_validator("image", mode="before")
    @classmethod
    def make_url(cls, value: StorageImage | None) -> HttpUrl | None:
        """Makes URL from DB path.

        FastAPI does NOT work properly with proxy, so for now protocol will be hardcoded.
        TODO: propagate forwarded headers, rely on trusted host.

        Args:
            value (fastapi_storages.StorageImage): Image field.

        Returns:
            ``pydantic.HttpUrl`` if Character has an image returns absolute URL to image and ``None`` otherwise.
        """
        if value is None:
            return None
        return build_url(path=value._name)  # noqa

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    def __init__(self, request: Request = None, **data: Any):
        self.request = request
        super().__init__(**data)


async def get_character(
    character_id: int,
    session: AsyncSession,
    /,
) -> Character:
    try:
        character: CharacterModel = await CharacterModel.get(session, character_id)
    except CharacterDoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Character.model_validate(character)


async def process_get_character(
    character_id: int,
    session: AsyncSession,
    /,
) -> Character:
    return await get_character(character_id, session)


async def process_get_characters(
    session: AsyncSession,
    /,
    *,
    gender: Optional[CharacterGenderFilter] = None,
    character_status: Optional[CharacterStatusFilter] = None,
    species: Optional[CharacterSpeciesFilter] = None,
    order_by: Optional[CharacterModel.order_by] = None,
    direction: Optional[OrderByDirection] = None,
    query: Optional[str] = None,
) -> Page[Character]:
    return await paginate(
        session,
        CharacterModel.get_filter_statement(
            order_by=order_by,
            order_by_direction=direction,
            gender=gender,
            character_statusx=character_status,
            species=species,
            query=query,
        ),
    )
