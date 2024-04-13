from typing import Any, Dict, Literal, Optional, Union
from datetime import datetime
from dataclasses import dataclass

from pydantic import BaseModel, Field, field_validator, model_validator

from python_fide.exceptions import InvalidFideIDError
from python_fide.constants.rating_cat import RatingCategory
from python_fide.utils.general import create_url
from python_fide.utils.types_utils import from_player_model
from python_fide.types_base import (
    FideEventDetailBase,
    FidePlayerBasicBase,
    FidePlayerDetailBase,
    FidePlayerGameBlackStatsBase,
    FidePlayerGameWhiteStatsBase,
    FidePlayerBase,
    FidePlayerRatingBase,
    FideTopPlayerBase
)
from python_fide.constants.common import (   
    FIDE_CALENDER_URL,
    FIDE_NEWS_URL
)

@dataclass
class URLInfo:
    url: str
    headers: Dict[str, str]


class FidePlayerName(BaseModel):
    first_name: str
    last_name: str

    @model_validator(mode='after')
    def validate_names(self) -> 'FidePlayerName':
        assert self.first_name.isalpha()
        assert self.last_name.isalpha()

        return self
    
    @property
    def search_name(self) -> str:
        return f'{self.last_name}, {self.first_name}'


class FideBaseID(BaseModel):
    entity_id: Union[str, int]

    @field_validator('entity_id', mode='after')
    @classmethod
    def cast_to_int(cls, entity_id: Union[str, int]) -> str:
        if isinstance(entity_id, str):
            assert entity_id.isdigit()

            try:
                entity_id = int(entity_id)
            except ValueError:
                raise InvalidFideIDError(
                    "invalid Fide ID entered, must be an equivalent integer"
                )

        return entity_id
    

class FidePlayerID(FideBaseID):
    pass


class FideNewsID(FideBaseID):
    pass


class FideEventID(FideBaseID):
    pass


class FidePlayerBasic(FidePlayerBasicBase):
    first_name: str
    last_name: str

    class Config:
        populate_by_name = True

    @classmethod
    def from_validated_model(cls, player: Dict[str, Any]) -> 'FidePlayerBasic':
        first_name, last_name, model = from_player_model(
            player=player,
            fide_player_model=FidePlayerBasicBase,
        )

        return cls(
            first_name=first_name, last_name=last_name, **model
        )


class FidePlayer(FidePlayerBase):
    first_name: str
    last_name: str

    class Config:
        populate_by_name = True

    @classmethod
    def from_validated_model(cls, player: Dict[str, Any]) -> 'FidePlayer':
        first_name, last_name, model = from_player_model(
            player=player,
            fide_player_model=FidePlayerBase,
        )

        return cls(
            first_name=first_name, last_name=last_name, **model
        )


class FideTopPlayer(FideTopPlayerBase):
    player: FidePlayerBasic
    category: RatingCategory

    class Config:
        populate_by_name = True
        use_enum_values = True

    @classmethod
    def from_validated_model(
        cls,
        player: Dict[str, Any],
        category: RatingCategory
    ) -> 'FideTopPlayer':
        fide_player = FidePlayerBasic.from_validated_model(player=player)
        fide_top_player = FideTopPlayerBase.model_validate(player)

        return cls(
            player=fide_player,
            category=category,
            **fide_top_player.model_dump()
        )


class FidePlayerDetail(FidePlayerDetailBase):
    player: FidePlayer

    class Config:
        populate_by_name = True

    @classmethod
    def from_validated_model(cls, player: Dict[str, Any]) -> 'FidePlayerDetail':
        fide_player = FidePlayer.from_validated_model(player=player)
        fide_player_detail = FidePlayerDetailBase.model_validate(player)

        return cls(
            player=fide_player,
            **fide_player_detail.model_dump()
        )
    

class FideEvent(BaseModel):
    name: str = Field(validation_alias='name')
    event_id: int = Field(validation_alias='id')

    @property
    def event_url(self) -> str:
        return create_url(
            base=FIDE_CALENDER_URL, segments=str(self.event_id)
        )


class FideNews(BaseModel):
    title: str = Field(validation_alias='name')
    news_id: int = Field(validation_alias='id')

    @property
    def news_url(self) -> str:
        return create_url(
            base=FIDE_NEWS_URL, segments=str(self.news_id)
        )


class FideEventDetail(FideEventDetailBase):
    event: FideEvent

    class Config:
        populate_by_name = True

    @classmethod
    def from_validated_model(cls, event: Dict[str, Any]) -> 'FideEventDetail':
        fide_event = FideEvent.model_validate(event)
        fide_event_detail = FideEventDetailBase.model_validate(event)
        return cls(
            event=fide_event,
            **fide_event_detail.model_dump()
        )


class FideRating(BaseModel):
    games: int
    rating: Optional[int]


class FidePlayerRating(BaseModel):
    month: str
    player: FidePlayer
    standard: FideRating
    rapid: FideRating
    blitz: FideRating

    @field_validator('month', mode='after')
    @classmethod
    def validate_month(cls, month: str) -> str:
        try:
            month_reformatted = datetime.strptime(month, '%Y-%b')
            month_date = datetime.strftime(month_reformatted, '%Y-%m-%d')
        except ValueError:
            raise ValueError(
                "'month' argument does not have expected date format '%Y-%b'"
            )
        else:
            return month_date
    
    @classmethod
    def from_validated_model(
        cls,
        player: FidePlayer, 
        rating: Dict[str, Any]
    ) -> 'FidePlayerRating':
        fide_rating = FidePlayerRatingBase.model_validate(rating)

        # Decompose the raw models into structured models
        standard_rating = FideRating(
            games=fide_rating.games_standard, rating=fide_rating.rating_standard
        )
        rapid_rating = FideRating(
            games=fide_rating.games_rapid, rating=fide_rating.rating_rapid
        )
        blitz_rating = FideRating(
            games=fide_rating.games_blitz, rating=fide_rating.rating_blitz
        )

        return cls(
            player=player,
            month=fide_rating.month,
            standard=standard_rating,
            rapid=rapid_rating,
            blitz=blitz_rating
        )

    @property
    def month_datetime(self) -> datetime:
        return datetime.strptime(self.month, '%Y-%m-%d')


class FideGames(BaseModel):
    games_total: int = Field(..., description='Number of total games played')
    games_won: int = Field(..., description='Number of games won')
    games_draw: int = Field(..., description='Number of games drawn')
    games_lost: int = Field(default=0, description='Number of games lost')

    @model_validator(mode='after')
    def validate_parameters(self) -> 'FideGames':
        self.games_lost = (
            self.games_total - self.games_won - self.games_draw
        )
        return self
    

class FideGamesSet(BaseModel):
    standard: FideGames
    rapid: FideGames
    blitz: FideGames


class FidePlayerGameStats(BaseModel):
    player: FidePlayer
    opponent: Optional[FidePlayer]
    white: FideGamesSet
    black: FideGamesSet

    @classmethod
    def from_validated_model(
        cls,
        fide_player: FidePlayer,
        fide_player_opponent: Optional[FidePlayer], 
        stats: Dict[str, Any]
    ) -> 'FidePlayerGameStats':
        
        def decompose_raw_stats(
            fide_stats: Union[
                FidePlayerGameBlackStatsBase,
                FidePlayerGameWhiteStatsBase
            ]
        ) -> FideGamesSet:
            return FideGamesSet(
                standard=FideGames(
                    games_total=fide_stats.standard,
                    games_won=fide_stats.standard_win, 
                    games_draw=fide_stats.standard_draw
                ),
                rapid=FideGames(
                    games_total=fide_stats.rapid,
                    games_won=fide_stats.rapid_win, 
                    games_draw=fide_stats.rapid_draw
                ),
                blitz=FideGames(
                    games_total=fide_stats.blitz,
                    games_won=fide_stats.blitz_win, 
                    games_draw=fide_stats.blitz_draw
                )
            )

        # Validate both white and black models
        stats_white = FidePlayerGameWhiteStatsBase.model_validate(stats)
        stats_black = FidePlayerGameBlackStatsBase.model_validate(stats)

        # Decompose the raw models into structured models
        stats_white_decomposed = decompose_raw_stats(
            fide_stats=stats_white
        )
        stats_black_decomposed = decompose_raw_stats(
            fide_stats=stats_black
        )

        return FidePlayerGameStats(
            opponent=fide_player,
            fide_player_opponent=fide_player_opponent,
            white=stats_white_decomposed,
            black=stats_black_decomposed
        )