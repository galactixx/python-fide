from abc import ABC, abstractmethod
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
    Union
)

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field, 
    field_validator, 
    HttpUrl
)

from python_fide.utils.general import clean_fide_player_name
from python_fide.types.annotated import (
    DateISO,
    DateTime,
    DateYear
)

class BaseRawModel(BaseModel):
    """
    Base model for all types. Sets model configuration and basic field validation.
    """
    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)

    @field_validator('*', mode='before')
    @classmethod
    def remove_null_strings(cls, value: Union[str, int]) -> Optional[Union[str, int]]:
        """Validation to replace any null strings with None."""
        if value == "":
            return None
        return value


class BaseRecordPaginationModel(ABC, BaseRawModel):
    """
    Base abstract model for any models to be directly validated by a single record
    through pagination.
    """
    @classmethod
    @abstractmethod
    def from_validated_model(cls, record: Dict[str, Any]) -> None:
        pass


class BasePlayer(BaseRawModel):
    """Base model for all player models."""
    def get_decomposed_player_name(self) -> Tuple[str, str]:
        return clean_fide_player_name(name=getattr(self, 'name'))

    def set_player_name(self, first_name: str, last_name: str) -> None:
        setattr(
            self, 'name', f'{first_name} {last_name}'
        )


class FidePlayerRaw(BasePlayer):
    """Raw model of the FidePlayer model."""
    name: str = Field(..., validation_alias='name')
    player_id: int = Field(..., validation_alias=AliasChoices('id', 'id_number'))
    title: Optional[str]
    country: str


class FidePlayerBasicRaw(BasePlayer):
    """Raw model of the FidePlayerBasic model."""
    name: str = Field(..., validation_alias='name')
    player_id: int = Field(..., validation_alias='id_number')
    country: str


class FideTopPlayerRaw(BaseRawModel):
    """Raw model of the FideTopPlayer model."""
    ranking: int = Field(..., validation_alias='pos')
    period: DateISO = Field(..., validation_alias='period_date')
    birthday: DateISO
    sex: Literal['M', 'F']
    rating_standard: Optional[int] = Field(..., validation_alias='rating')
    rating_rapid: Optional[int] = Field(..., validation_alias='rapid_rating')
    rating_blitz: Optional[int] = Field(..., validation_alias='blitz_rating')


class FidePlayerDetailRaw(BaseRawModel):
    """Raw model of the FidePlayerDetail model."""
    sex: Literal['M', 'F']
    birth_year: DateYear = Field(..., validation_alias='birthyear')
    rating_standard: Optional[int] = Field(..., validation_alias='standard_rating')
    rating_rapid: Optional[int] = Field(..., validation_alias='rapid_rating')
    rating_blitz: Optional[int] = Field(..., validation_alias='blitz_rating')


class FideEventDetailRaw(BaseRawModel):
    """Raw model of the FideEventDetail model."""
    city: Optional[str]
    country: Optional[str]
    start_date: Optional[DateTime] = Field(..., validation_alias='date_start')
    end_date: Optional[DateTime] = Field(..., validation_alias='date_end')
    game_format: str = Field(..., validation_alias='time_control_typ')
    tournament_type: Optional[str] = Field(..., validation_alias='tournament_system')
    time_control: Optional[str] = Field(..., validation_alias='time_control')
    time_control_desc: Optional[str] = Field(..., validation_alias='timecontrol_description')
    rounds: Optional[str] = Field(..., validation_alias='num_round')
    players: Optional[str] = Field(..., validation_alias='number_of_players')
    telephone: Optional[str] = Field(..., validation_alias='tel')
    website: Optional[str]
    organizer: Optional[str]
    chief_arbiter: Optional[str]
    chief_organizer: Optional[str]


class FideNewsImage(BaseRawModel):
    """Model for an image included in the FideNewsDetail model."""
    image_type: str = Field(..., validation_alias='type')
    image_size: str = Field(..., validation_alias='size')
    image_url: HttpUrl = Field(..., validation_alias='url')


class FideNewsContent(BaseRawModel):
    """
    Model representing a content element, including text content and any images.
    """
    content: str
    images: List[FideNewsImage]


class FideNewsTopic(BaseRawModel):
    """Model representing a news topic."""
    topic_id: int = Field(..., validation_alias='id')
    topic_name: str = Field(..., validation_alias='name')


class FideNewsCategory(BaseRawModel):
    """Model representing a news category."""
    category_id: int = Field(..., validation_alias='id')
    category_name: str = Field(..., validation_alias='name')


class FideNewsDetailRaw(BaseRawModel):
    """Raw model of the FideNewsDetail model."""
    topic: FideNewsTopic
    category: FideNewsCategory
    contents: List[FideNewsContent]
    created_at: DateTime
    updated_at: DateTime


class FidePlayerRatingRaw(BaseRawModel):
    """Raw model used in validating the FidePlayerRating model."""
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
        """Validator to return a 0 if the value is None."""
        return value or 0


class FidePlayerGameWhiteStatsRaw(BaseRawModel):
    """Raw model used in validating the white game stats fields in the FidePlayerGameStats model."""
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
        """Validator to return a 0 if the value is None."""
        return value or 0


class FidePlayerGameBlackStatsRaw(BaseRawModel):
    """Raw model used in validating the black game stats fields in the FidePlayerGameStats model."""
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
        """Validator to return a 0 if the value is None."""
        return value or 0