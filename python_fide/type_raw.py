from typing import Any, Optional

from pydantic import BaseModel, Field

from python_fide.utils.pydantic import assign_default_if_none

class FidePlayerRaw(BaseModel):
    name: str = Field(validation_alias='name')
    player_id: str = Field(validation_alias='id')
    title: Optional[str]
    country: str


class FidePlayerRatingRaw(BaseModel):
    month: str = Field(validation_alias='date_2')
    rating_standard: Optional[int] = Field(validation_alias='rating')
    rating_rapid: Optional[int] = Field(validation_alias='rapid_rtng')
    rating_blitz: Optional[int] = Field(validation_alias='blitz_rtng')
    games_standard: Optional[int] = Field(default=0, validation_alias='period_games')
    games_rapid: Optional[int] = Field(default=0, validation_alias='rapid_games')
    games_blitz: Optional[int] = Field(default=0, validation_alias='blitz_games')

    def model_post_init(self, __context: Any):
        assign_default_if_none(model=self)