from typing import Any, Dict, Optional, Union

from pydantic import Field, field_validator

from python_fide.utils.general import build_url
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
    fide_player_id: int = Field(..., alias='event')
    period: Optional[Period] = Field(..., alias='period')

    @field_validator('period', mode='after')
    @classmethod
    def validate_period(cls, period: Optional[Period]) -> Period:
        """
        """
        if period is None:
            period = Period.ALL_YEARS
        return period

    @classmethod
    def from_player_object(
        cls,
        period: Optional[Period],
        fide_player: Union[FidePlayer, FidePlayerID]
    ) -> 'PlayerChartsConfig':
        """
        """
        fide_player_id = parse_fide_player(fide_player=fide_player)
        return cls(
            fide_player_id=fide_player_id, period=period
        )

    @property
    def parameterize(self) -> Dict[str, Any]:
        """
        """
        return self.model_dump(by_alias=True)


class PlayerStatsConfig(BaseParameterConfig):
    """
    """
    fide_player_id: int = Field(..., alias='id1')
    fide_player_opponent_id: Optional[int] = Field(..., alias='id2')

    @classmethod
    def from_player_object(
        cls,
        fide_player: Union[FidePlayer, FidePlayerID],
        fide_player_opponent: Optional[Union[FidePlayer, FidePlayerID]]
    ) -> 'PlayerStatsConfig':
        """
        """
        fide_player_id = parse_fide_player(fide_player=fide_player)

        if fide_player_opponent is None:
            fide_player_opponent_id = None
        else:
            fide_player_opponent_id = parse_fide_player(
                fide_player=fide_player_opponent
            )
        return cls(
            fide_player_id=fide_player_id,
            fide_player_opponent_id=fide_player_opponent_id
        )

    @property
    def parameterize(self) -> Dict[str, Any]:
        """
        """
        return self.model_dump(by_alias=True)
    

class PlayerDetailConfig(BaseEndpointConfig):
    """
    """
    fide_player_id: int

    @classmethod
    def from_player_object(
        cls,
        fide_player: Union[FidePlayer, FidePlayerID]
    ) -> 'PlayerDetailConfig':
        fide_player_id = parse_fide_player(fide_player=fide_player)
        return cls(
            fide_player_id=fide_player_id
        )
    
    def endpointize(self, base_url: str) -> str:
        return build_url(
            base=base_url, segments=self.fide_player_id
        )
    

class PlayerOpponentsConfig(BaseParameterConfig):
    """
    """
    fide_player_id: int = Field(..., alias='pl')

    @classmethod
    def from_player_object(
        cls,
        fide_player: Union[FidePlayer, FidePlayerID]
    ) -> 'PlayerOpponentsConfig':
        fide_player_id = parse_fide_player(fide_player=fide_player)
        return cls(
            fide_player_id=fide_player_id
        )
    
    @property
    def parameterize(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True)