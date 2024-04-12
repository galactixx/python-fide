from typing import Any, Dict, Literal, Optional, Union
from datetime import datetime
from dataclasses import dataclass

from pydantic import BaseModel, Field, field_validator, model_validator

from python_fide.constants.rating_cat import RatingCategory
from python_fide.utils.general import (
    clean_fide_player_name,
    create_url
)
from python_fide.types_base import (
    FidePlayerDetailRaw,
    FidePlayerGameBlackStatsRaw,
    FidePlayerGameWhiteStatsRaw,
    FidePlayerBase,
    FidePlayerRatingRaw,
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
    def cast_to_string(cls, entity_id: Union[str, int]) -> str:
        if isinstance(entity_id, int):
            entity_id = str(entity_id)

        assert entity_id.isdigit()

        return entity_id
    

class FidePlayerID(FideBaseID):
    pass


class FideNewsID(FideBaseID):
    pass


class FideEventID(FideBaseID):
    pass


class FideTopPlayer(FideTopPlayerBase):
    category: RatingCategory
    first_name: str
    last_name: str

    class Config:
        populate_by_name = True
        use_enum_values = True

    @classmethod
    def from_validated_model(
        cls,
        player: Dict[str, Any],
        category: RatingCategory
    ) -> 'FideTopPlayer':
        fide_player = FideTopPlayerBase.model_validate(player)

        # Generate cleaned name variables based on raw JSON
        # name output from API
        player_first_name, player_last_name = clean_fide_player_name(
            name=fide_player.name
        )

        # Reset the player name attribute
        fide_player.set_player_name(
            first_name=player_first_name, last_name=player_last_name
        )

        return cls(
            category=category,
            first_name=player_first_name,
            last_name=player_last_name,
            **fide_player.model_dump()
        )


class FidePlayer(FidePlayerBase):
    first_name: str
    last_name: str

    class Config:
        populate_by_name = True

    @classmethod
    def from_validated_model(cls, player: Dict[str, Any]) -> 'FidePlayer':
        fide_player = FidePlayerBase.model_validate(player)

        # Generate cleaned name variables based on raw JSON
        # name output from API
        player_first_name, player_last_name = clean_fide_player_name(
            name=fide_player.name
        )

        # Reset the player name attribute
        fide_player.set_player_name(
            first_name=player_first_name, last_name=player_last_name
        )

        return cls(
            first_name=player_first_name,
            last_name=player_last_name,
            **fide_player.model_dump()
        )
    

class FidePlayerDetail(BaseModel):
    player: FidePlayer
    sex: Literal['M', 'F']
    birth_year: str
    rating_standard: Optional[int]
    rating_rapid: Optional[int]
    rating_blitz: Optional[int]

    @classmethod
    def from_validated_model(cls, player: Dict[str, Any]) -> 'FidePlayerDetail':
        fide_player = FidePlayer.from_validated_model(player=player)
        fide_player_detail = FidePlayerDetailRaw.model_validate(player)

        return cls(
            player=fide_player,
            **fide_player_detail.model_dump()
        )


class FideEvent(BaseModel):
    name: str = Field(validation_alias='name')
    event_id: str = Field(validation_alias='id')

    @property
    def event_url(self) -> str:
        return create_url(
            base=FIDE_CALENDER_URL, segments=self.event_id
        )


class FideNews(BaseModel):
    title: str = Field(validation_alias='name')
    news_id: str = Field(validation_alias='id')

    @property
    def news_url(self) -> str:
        return create_url(
            base=FIDE_NEWS_URL, segments=self.news_id
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
        fide_rating = FidePlayerRatingRaw.model_validate(rating)

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
            fide_stats: Union[FidePlayerGameBlackStatsRaw, FidePlayerGameWhiteStatsRaw]
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
        stats_white = FidePlayerGameWhiteStatsRaw.model_validate(stats)
        stats_black = FidePlayerGameBlackStatsRaw.model_validate(stats)

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