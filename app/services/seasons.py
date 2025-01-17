from typing import List

from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.repositories.models import (
    Season as SeasonModel,
    SeasonDoesNotExist,
)
from app.services.base import EpisodeBase


class EpisodeSeason(EpisodeBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class Season(BaseModel):
    id: int
    episodes: List[EpisodeSeason]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


async def process_get_season(
    season_id: int,
    session: AsyncSession,
    /,
) -> Season:
    try:
        season: SeasonModel = await SeasonModel.get(session, season_id)
    except SeasonDoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Season.model_validate(season)


async def process_get_seasons(session: AsyncSession, /) -> Page[Season]:
    return await paginate(
        session,
        SeasonModel.get_filter_statement(
            select_in_load=SeasonModel.episodes,
        ),
    )
