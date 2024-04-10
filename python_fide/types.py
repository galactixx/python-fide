from typing import Any, Dict, Literal, Optional, Union
from datetime import datetime
from dataclasses import dataclass

from pydantic import BaseModel, Field, field_validator, model_validator

from python_fide.exceptions import IncorrectAttrError
from python_fide.utils import create_url
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


class FidePlayer(BaseModel):
    _name: str = Field(validation_alias='name')
    player_id: str = Field(validation_alias='id')
    title: Optional[str]
    country: str

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    @property
    def first_name(self) -> str:
        return ' '.join(
            name.strip() for name in self._name.split(',')[1:]
        )

    @property
    def last_name(self) -> str:
        return self._name.split(',')[0].strip()
    

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
    

class FidePlayerRating(BaseModel):
    player: FidePlayer
    month: str = Field(validation_alias='date_2')
    rating_standard: Optional[int] = Field(validation_alias='rating')
    rating_rapid: Optional[int] = Field(validation_alias='rapid_rtng')
    rating_blitz: Optional[int] = Field(validation_alias='blitz_rtng')
    games_standard: Optional[int] = Field(validation_alias='period_games')
    games_rapid: Optional[int] = Field(validation_alias='rapid_games')
    games_blitz: Optional[int] = Field(validation_alias='blitz_games')

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
    
    @property
    def month_datetime(self) -> datetime:
        return datetime.strptime(self.month, '%Y-%m-%d')


class FideGames(BaseModel):
    games_total: int = Field(description='Number of total games played')
    games_won: int = Field(description='Number of games won')
    games_draw: int = Field(description='Number of games drawn')
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
    opponent: Optional[FidePlayer]
    white: FideGamesSet
    black: FideGamesSet


class _FidePlayerGameStatsRaw(BaseModel):
    opponent: Optional[FidePlayer] = None
    white_total: Optional[int] = Field(default=0)
    white_total_win: Optional[int] = Field(default=0, validation_alias='white_win_num')
    white_total_draw: Optional[int] = Field(default=0, validation_alias='white_draw_num')
    white_standard: Optional[int] = Field(default=0, validation_alias='white_total_std')
    white_standard_win: Optional[int] = Field(default=0, validation_alias='white_win_num_std')
    white_standard_draw: Optional[int] = Field(default=0, validation_alias='white_draw_num_std')
    white_rapid: Optional[int] = Field(default=0, validation_alias='white_total_rpd')
    white_rapid_win: Optional[int] = Field(default=0, validation_alias='white_win_num_rpd')
    white_rapid_draw: Optional[int] = Field(default=0, validation_alias='white_draw_num_rpd')
    white_blitz: Optional[int] = Field(default=0, validation_alias='white_total_blz')
    white_blitz_win: Optional[int] = Field(default=0, validation_alias='white_win_num_blz')
    white_blitz_draw: Optional[int] = Field(default=0, validation_alias='white_draw_num_blz')
    black_total: Optional[int] = Field(default=0)
    black_total_win: Optional[int] = Field(default=0, validation_alias='black_win_num')
    black_total_draw: Optional[int] = Field(default=0, validation_alias='black_draw_num')
    black_standard: Optional[int] = Field(default=0, validation_alias='black_total_std')
    black_standard_win: Optional[int] = Field(default=0, validation_alias='black_win_num_std')
    black_standard_draw: Optional[int] = Field(default=0, validation_alias='black_draw_num_std')
    black_rapid: Optional[int] = Field(default=0, validation_alias='black_total_rpd')
    black_rapid_win: Optional[int] = Field(default=0, validation_alias='black_win_num_rpd')
    black_rapid_draw: Optional[int] = Field(default=0, validation_alias='black_draw_num_rpd')
    black_blitz: Optional[int] = Field(default=0, validation_alias='black_total_blz')
    black_blitz_win: Optional[int] = Field(default=0, validation_alias='black_win_num_blz')
    black_blitz_draw: Optional[int] = Field(default=0, validation_alias='black_draw_num_blz')

    def model_post_init(self, __context: Any):
        for field_name, field_info in self.model_fields.items():
            field_value = getattr(self, field_name)
            if field_value is None:
                setattr(self, field_name, field_info.default)

    def _to_fide_games(
        self,
        game_color: Literal['white', 'black'],
        game_format: Literal['standard', 'rapid', 'blitz']
    ) -> FideGames:
        try:
            games_total = getattr(self, f'{game_color}_{game_format}')
            games_won = getattr(self, f'{game_color}_{game_format}_win')
            games_draw = getattr(self, f'{game_color}_{game_format}_draw')
        except AttributeError:
            raise IncorrectAttrError()
        else:
            return FideGames(
                games_total=games_total, games_won=games_won, games_draw=games_draw
            )

    def _to_fide_games_set(
        self,
        game_color: Literal['white', 'black']
    ) -> FideGamesSet:
        return FideGamesSet(
            standard=self._to_fide_games(
                game_color=game_color, game_format='standard'
            ),
            rapid=self._to_fide_games(
                game_color=game_color, game_format='rapid'
            ),
            blitz=self._to_fide_games(
                game_color=game_color, game_format='blitz'
            ),
        )

    def to_complete_stats(self) -> FidePlayerGameStats:
        return FidePlayerGameStats(
            opponent=self.opponent,
            white=self._to_fide_games_set(game_color='white'),
            black=self._to_fide_games_set(game_color='black')
        )
        