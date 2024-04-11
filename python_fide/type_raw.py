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


class FidePlayerGameWhiteStatsRaw(BaseModel):
    total: Optional[int] = Field(default=0)
    total_win: Optional[int] = Field(default=0, validation_alias='white_win_num')
    total_draw: Optional[int] = Field(default=0, validation_alias='white_draw_num')
    standard: Optional[int] = Field(default=0, validation_alias='white_total_std')
    standard_win: Optional[int] = Field(default=0, validation_alias='white_win_num_std')
    standard_draw: Optional[int] = Field(default=0, validation_alias='white_draw_num_std')
    rapid: Optional[int] = Field(default=0, validation_alias='white_total_rpd')
    rapid_win: Optional[int] = Field(default=0, validation_alias='white_win_num_rpd')
    rapid_draw: Optional[int] = Field(default=0, validation_alias='white_draw_num_rpd')
    blitz: Optional[int] = Field(default=0, validation_alias='white_total_blz')
    blitz_win: Optional[int] = Field(default=0, validation_alias='white_win_num_blz')
    blitz_draw: Optional[int] = Field(default=0, validation_alias='white_draw_num_blz')

    def model_post_init(self, __context: Any):
        assign_default_if_none(model=self)


class FidePlayerGameBlackStatsRaw(BaseModel):
    total: Optional[int] = Field(default=0)
    total_win: Optional[int] = Field(default=0, validation_alias='black_win_num')
    total_draw: Optional[int] = Field(default=0, validation_alias='black_draw_num')
    standard: Optional[int] = Field(default=0, validation_alias='black_total_std')
    standard_win: Optional[int] = Field(default=0, validation_alias='black_win_num_std')
    standard_draw: Optional[int] = Field(default=0, validation_alias='black_draw_num_std')
    rapid: Optional[int] = Field(default=0, validation_alias='black_total_rpd')
    rapid_win: Optional[int] = Field(default=0, validation_alias='black_win_num_rpd')
    rapid_draw: Optional[int] = Field(default=0, validation_alias='black_draw_num_rpd')
    blitz: Optional[int] = Field(default=0, validation_alias='black_total_blz')
    blitz_win: Optional[int] = Field(default=0, validation_alias='black_win_num_blz')
    blitz_draw: Optional[int] = Field(default=0, validation_alias='black_draw_num_blz')

    def model_post_init(self, __context: Any):
        assign_default_if_none(model=self)