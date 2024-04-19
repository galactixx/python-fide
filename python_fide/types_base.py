from typing import Any, List, Literal, Optional, Tuple, Union

from pydantic import AliasChoices, BaseModel, Field, field_validator, HttpUrl

from python_fide.utils.general import (
    clean_fide_player_name,
    remove_non_digits_from_string,
    validate_date_format
)

class BaseRawModel(BaseModel):
    @field_validator('*', mode='before')
    @classmethod
    def remove_null_strings(cls, value: Any) -> Any:
        if value == "":
            return None
        return value

    class Config:
        populate_by_name = True
        run_validators = True


class BasePlayer(BaseRawModel):
    def get_decomposed_player_name(self) -> Tuple[str, str]:
        return clean_fide_player_name(
            name=getattr(self, 'name')
        )

    def set_player_name(self, first_name: str, last_name: str) -> None:
        setattr(
            self, 'name', f'{first_name} {last_name}'
        )


class FidePlayerBase(BasePlayer):
    name: str = Field(..., validation_alias='name')
    player_id: int = Field(..., validation_alias=AliasChoices('id', 'id_number'))
    title: Optional[str]
    country: str


class FidePlayerBasicBase(BasePlayer):
    name: str = Field(..., validation_alias='name')
    player_id: int = Field(..., validation_alias='id_number')
    country: str


class FideTopPlayerBase(BaseRawModel):
    ranking: int = Field(..., validation_alias='pos')
    period: str = Field(..., validation_alias='period_date')
    birthday: str
    sex: Literal['M', 'F']
    rating_standard: Optional[int] = Field(..., validation_alias='rating')
    rating_rapid: Optional[int] = Field(..., validation_alias='rapid_rating')
    rating_blitz: Optional[int] = Field(..., validation_alias='blitz_rating')

    @field_validator('birthday', 'period', mode='after')
    @classmethod
    def validate_date_format(cls, date: str) -> Optional[str]:
        if cls.Config.run_validators:
            return validate_date_format(date=date, date_format='%Y-%m-%d')
        return date


class FidePlayerDetailBase(BaseRawModel):
    sex: Literal['M', 'F']
    birth_year: str = Field(..., validation_alias='birthyear')
    rating_standard: Optional[int] = Field(..., validation_alias='standard_rating')
    rating_rapid: Optional[int] = Field(..., validation_alias='rapid_rating')
    rating_blitz: Optional[int] = Field(..., validation_alias='blitz_rating')

    @field_validator('birth_year',  mode='after')
    @classmethod
    def validate_date_format(cls, date: str) -> Optional[str]:
        if cls.Config.run_validators:
            return validate_date_format(date=date, date_format='%Y')
        return date


class FideEventDetailBase(BaseRawModel):
    city: Optional[str]
    country: Optional[str]
    description: Optional[str] = Field(..., validation_alias='remarks')
    start_date: Optional[str] = Field(..., validation_alias='date_start')
    end_date: Optional[str] = Field(..., validation_alias='date_end')
    game_format: str = Field(..., validation_alias='time_control_typ')
    tournament_type: Optional[str] = Field(..., validation_alias='tournament_system')
    time_control: Optional[str] = Field(..., validation_alias='time_control')
    time_control_desc: Optional[str] = Field(..., validation_alias='timecontrol_description')
    rounds: Optional[int] = Field(..., validation_alias='num_round')
    players: Optional[int] = Field(..., validation_alias='number_of_players')
    telephone: Optional[str] = Field(..., validation_alias='tel')
    website: Optional[HttpUrl]
    organizer: Optional[str]
    chief_arbiter: Optional[str]
    chief_organizer: Optional[str]

    @field_validator('players', 'rounds', mode='before')
    @classmethod
    def remove_characters(cls, value: Union[str, int]) -> str:
        if cls.Config.run_validators:
            if isinstance(value, str):
                return remove_non_digits_from_string(text=value)
        return value

    @field_validator('start_date', 'end_date', mode='after')
    @classmethod
    def validate_date_format(cls, date: str) -> Optional[str]:
        if cls.Config.run_validators:
            return validate_date_format(
                date=date, date_format='%Y-%m-%d %H:%M:%S'
            )
        return date


class FideNewsImage(BaseRawModel):
    image_type: str = Field(..., validation_alias='type')
    image_size: str = Field(..., validation_alias='size')
    image_url: HttpUrl = Field(..., validation_alias='url')


class FideNewsContent(BaseRawModel):
    content: str
    images: List[FideNewsImage]


class FideNewsTopic(BaseRawModel):
    topic_id: int = Field(..., validation_alias='id')
    topic_name: str = Field(..., validation_alias='name')


class FideNewsCategory(BaseRawModel):
    category_id: int = Field(..., validation_alias='id')
    category_name: str = Field(..., validation_alias='name')


class FideNewsDetailBase(BaseRawModel):
    topic: FideNewsTopic
    category: FideNewsCategory
    contents: List[FideNewsContent]
    posted_at: str
    created_at: str
    updated_at: str

    @field_validator(
        'posted_at', 'created_at', 'updated_at', mode='after'
    )
    @classmethod
    def validate_date_format(cls, date: str) -> Optional[str]:
        if cls.Config.run_validators:
            return validate_date_format(
                date=date, date_format='%Y-%m-%d %H:%M:%S'
            )
        return date


class FidePlayerRatingBase(BaseRawModel):
    month: str = Field(..., validation_alias='date_2')
    rating_standard: Optional[int] = Field(..., validation_alias='rating')
    rating_rapid: Optional[int] = Field(..., validation_alias='rapid_rtng')
    rating_blitz: Optional[int] = Field(..., validation_alias='blitz_rtng')
    games_standard: Optional[int] = Field(..., validation_alias='period_games')
    games_rapid: Optional[int] = Field(..., validation_alias='rapid_games')
    games_blitz: Optional[int] = Field(..., validation_alias='blitz_games')

    @field_validator(
        'games_standard', 'games_rapid', 'games_blitz', mode='after'
    )
    @classmethod
    def override_none(cls, value: Optional[int]) -> int:
        return value or 0


class FidePlayerGameWhiteStatsBase(BaseRawModel):
    total: Optional[int] = Field(..., validation_alias='white_total')
    total_win: Optional[int] = Field(..., validation_alias='white_win_num')
    total_draw: Optional[int] = Field(..., validation_alias='white_draw_num')
    standard: Optional[int] = Field(..., validation_alias='white_total_std')
    standard_win: Optional[int] = Field(..., validation_alias='white_win_num_std')
    standard_draw: Optional[int] = Field(..., validation_alias='white_draw_num_std')
    rapid: Optional[int] = Field(..., validation_alias='white_total_rpd')
    rapid_win: Optional[int] = Field(..., validation_alias='white_win_num_rpd')
    rapid_draw: Optional[int] = Field(..., validation_alias='white_draw_num_rpd')
    blitz: Optional[int] = Field(..., validation_alias='white_total_blz')
    blitz_win: Optional[int] = Field(..., validation_alias='white_win_num_blz')
    blitz_draw: Optional[int] = Field(..., validation_alias='white_draw_num_blz')

    @field_validator('*', mode='after')
    @classmethod
    def override_none(cls, value: Optional[int]) -> int:
        return value or 0


class FidePlayerGameBlackStatsBase(BaseRawModel):
    total: Optional[int] = Field(..., validation_alias='black_total')
    total_win: Optional[int] = Field(..., validation_alias='black_win_num')
    total_draw: Optional[int] = Field(..., validation_alias='black_draw_num')
    standard: Optional[int] = Field(..., validation_alias='black_total_std')
    standard_win: Optional[int] = Field(..., validation_alias='black_win_num_std')
    standard_draw: Optional[int] = Field(..., validation_alias='black_draw_num_std')
    rapid: Optional[int] = Field(..., validation_alias='black_total_rpd')
    rapid_win: Optional[int] = Field(..., validation_alias='black_win_num_rpd')
    rapid_draw: Optional[int] = Field(..., validation_alias='black_draw_num_rpd')
    blitz: Optional[int] = Field(..., validation_alias='black_total_blz')
    blitz_win: Optional[int] = Field(..., validation_alias='black_win_num_blz')
    blitz_draw: Optional[int] = Field(..., validation_alias='black_draw_num_blz')

    @field_validator('*', mode='after')
    @classmethod
    def override_none(cls, value: Optional[int]) -> int:
        return value or 0