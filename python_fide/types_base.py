from typing import Any, Literal, Optional

from pydantic import AliasChoices, BaseModel, Field

from python_fide.utils.pydantic import assign_default_if_none

class BaseRawModel(BaseModel):
    def model_post_init(self, __context: Any):
        assign_default_if_none(model=self)


class FidePlayerBase(BaseRawModel):
    name: str = Field(..., validation_alias='name')
    player_id: str = Field(..., validation_alias=AliasChoices('id', 'id_number'))
    title: Optional[str]
    country: str

    def set_player_name(
        self,
        first_name: str, 
        last_name: str
    ) -> None:
        setattr(
            self, 'name', f'{first_name} {last_name}'
        )
    

class FidePlayerTopBase(BaseRawModel):
    ranking: int = Field(..., validation_alias='pos')
    period: str = Field(..., validation_alias='period_date')
    player_id: str = Field(..., validation_alias='id_number')
    name: str
    country: str
    birthday: str
    sex: Literal['M', 'F']
    rating_standard: Optional[int] = Field(default=None, validation_alias='rating')
    rating_rapid: Optional[int] = Field(default=None, validation_alias='rapid_rating')
    rating_blitz: Optional[int] = Field(default=None, validation_alias='blitz_rating')

    def set_player_name(
        self, 
        first_name: str, 
        last_name: str
    ) -> None:
        setattr(
            self, 'name', f'{first_name} {last_name}'
        )


class FidePlayerDetailRaw(BaseRawModel):
    sex: Literal['M', 'F']
    birth_year: str = Field(..., validation_alias='birthyear')
    rating_standard: Optional[int] = Field(..., validation_alias='standard_rating')
    rating_rapid: Optional[int] = Field(..., validation_alias='rapid_rating')
    rating_blitz: Optional[int] = Field(..., validation_alias='blitz_rating')


class FidePlayerRatingRaw(BaseRawModel):
    month: str = Field(..., validation_alias='date_2')
    rating_standard: Optional[int] = Field(..., validation_alias='rating')
    rating_rapid: Optional[int] = Field(..., validation_alias='rapid_rtng')
    rating_blitz: Optional[int] = Field(..., validation_alias='blitz_rtng')
    games_standard: Optional[int] = Field(default=0, validation_alias='period_games')
    games_rapid: Optional[int] = Field(default=0, validation_alias='rapid_games')
    games_blitz: Optional[int] = Field(default=0, validation_alias='blitz_games')


class FidePlayerGameWhiteStatsRaw(BaseRawModel):
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


class FidePlayerGameBlackStatsRaw(BaseRawModel):
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