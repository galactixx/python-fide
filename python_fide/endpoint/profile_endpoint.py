from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field, field_validator

from python_fide.constants.common import FIDE_PLAYER_DETAIL_URL
from python_fide.utils.general import create_url
from python_fide.utils.config import parse_fide_player
from python_fide.constants.periods import Period
from python_fide.endpoint.base_endpoint import BaseConfig
from python_fide.types import (
    FidePlayer,
    FidePlayerID
)

class ProfileChartsConfig(BaseConfig):
    fide_player: Union[
        FidePlayer, 
        FidePlayerID
    ] = Field(..., alias='event')
    period: Optional[Period] = Field(..., alias='period')

    @field_validator('period', mode='after')
    @classmethod
    def validate_period(cls, period: Optional[Period]) -> Period:
        if period is not None:
            period = Period.ALL_YEARS
        return period

    @field_validator('fide_player', mode='after')
    @classmethod
    def extract_fide_id(
        cls,
        fide_player: Union[FidePlayer, FidePlayerID]
    ) -> str:
        player_id = parse_fide_player(fide_player=fide_player)
        return player_id

    @property
    def parameterize(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True)


class ProfileStatsConfig(BaseConfig):
    fide_player: Union[
        FidePlayer, 
        FidePlayerID
    ] = Field(..., alias='id1')
    fide_player_opponent: Optional[
        Union[FidePlayer, FidePlayerID]
    ] = Field(..., alias='id2')

    @field_validator('fide_player', mode='after')
    @classmethod
    def extract_fide_id(
        cls,
        fide_player: Union[FidePlayer, FidePlayerID]
    ) -> str:
        player_id = parse_fide_player(fide_player=fide_player)
        return player_id

    @field_validator('fide_player_opponent', mode='after')
    @classmethod
    def extract_fide_id_from_opponent(
        cls,
        fide_player_opponent: Optional[
            Union[FidePlayer, FidePlayerID]
        ]
    ) -> str:
        if fide_player_opponent is not None:
            player_id = parse_fide_player(
                fide_player=fide_player_opponent
            )
            return player_id
        return fide_player_opponent

    @property
    def parameterize(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True)
    

class ProfileDetailConfig(BaseModel):
    fide_player: Union[
        FidePlayer, 
        FidePlayerID
    ]

    @field_validator('fide_player', mode='after')
    @classmethod
    def extract_fide_id(
        cls,
        fide_player: Union[FidePlayer, FidePlayerID]
    ) -> str:
        player_id = parse_fide_player(fide_player=fide_player)
        return player_id
    
    @property
    def endpointize(self) -> str:
        return create_url(
            base=FIDE_PLAYER_DETAIL_URL,
            segments=self.fide_player
        )