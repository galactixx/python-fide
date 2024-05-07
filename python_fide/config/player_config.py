from typing import Optional
from typing_extensions import Annotated

from pydantic import Field, field_validator
from pydantic.functional_validators import BeforeValidator

from python_fide.utils.general import build_url
from python_fide.enums import Period
from python_fide.utils.config import (
    parse_fide_player,
    parse_fide_player_optional
)
from python_fide.config.base_config import (
    BaseEndpointConfig,
    ParameterAliasConfig
)

FideID = Annotated[int, BeforeValidator(parse_fide_player)]
FideIDOptional = Annotated[
    Optional[int], BeforeValidator(parse_fide_player_optional)
]

class PlayerOpponentsConfig(ParameterAliasConfig):
    """
    """
    fide_player_id: FideID = Field(..., alias='pl')


class PlayerChartsConfig(ParameterAliasConfig):
    """
    """
    fide_player_id: FideID = Field(..., alias='event')
    period: Optional[Period] = Field(..., alias='period')

    @field_validator('period', mode='after')
    @classmethod
    def validate_period(cls, period: Optional[Period]) -> Period:
        """
        """
        if period is None:
            period = Period.ALL_YEARS
        return period


class PlayerStatsConfig(ParameterAliasConfig):
    """
    """
    fide_player_id: FideID = Field(..., alias='id1')
    fide_player_opponent_id: FideIDOptional = Field(default=None, alias='id2')
    

class PlayerDetailConfig(BaseEndpointConfig):
    """
    """
    fide_player_id: FideID
    
    def endpointize(self, base_url: str) -> str:
        """
        """
        return build_url(
            base=base_url, segments=self.fide_player_id
        )