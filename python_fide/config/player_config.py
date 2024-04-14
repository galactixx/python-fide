from typing import Any, Dict, Optional, Union

from pydantic import Field, field_validator

from python_fide.utils.general import create_url
from python_fide.utils.config import parse_fide_player
from python_fide.enums import Period
from python_fide.config.base_config import (
    BaseParameterConfig,
    BaseEndpointConfig
)
from python_fide.types import (
    FidePlayer,
    FidePlayerID
)

class PlayerChartsConfig(BaseParameterConfig):
    """
    """
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
    ) -> int:
        player_id = parse_fide_player(fide_player=fide_player)
        return player_id

    @property
    def parameterize(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True)


class PlayerStatsConfig(BaseParameterConfig):
    """
    """
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
    ) -> int:
        player_id = parse_fide_player(fide_player=fide_player)
        return player_id

    @field_validator('fide_player_opponent', mode='after')
    @classmethod
    def extract_fide_id_from_opponent(
        cls,
        fide_player_opponent: Optional[
            Union[FidePlayer, FidePlayerID]
        ]
    ) -> Optional[int]:
        if fide_player_opponent is not None:
            player_id = parse_fide_player(
                fide_player=fide_player_opponent
            )
            return player_id
        return fide_player_opponent

    @property
    def parameterize(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True)
    

class PlayerDetailConfig(BaseEndpointConfig):
    """
    """
    fide_player: Union[
        FidePlayer, 
        FidePlayerID
    ]

    @field_validator('fide_player', mode='after')
    @classmethod
    def extract_fide_id(
        cls,
        fide_player: Union[FidePlayer, FidePlayerID]
    ) -> int:
        player_id = parse_fide_player(fide_player=fide_player)
        return player_id
    
    def endpointize(self, base_url: str) -> str:
        return create_url(
            base=base_url, segments=self.fide_player
        )
    

class PlayerOpponentsConfig(BaseParameterConfig):
    """
    """
    fide_player: Union[
        FidePlayer, 
        FidePlayerID
    ] = Field(..., alias='pl')

    @field_validator('fide_player', mode='after')
    @classmethod
    def extract_fide_id(
        cls,
        fide_player: Union[FidePlayer, FidePlayerID]
    ) -> int:
        player_id = parse_fide_player(fide_player=fide_player)
        return player_id
    
    @property
    def parameterize(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True)