from typing import Any, Dict, Optional
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
    BaseParameterConfig,
    BaseEndpointConfig
)

FideID = Annotated[int, BeforeValidator(parse_fide_player)]
FideIDOptional = Annotated[
    Optional[int], BeforeValidator(parse_fide_player_optional)
]

class PlayerChartsConfig(BaseParameterConfig):
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

    @property
    def parameterize(self) -> Dict[str, Any]:
        """
        """
        return self.model_dump(by_alias=True)


class PlayerStatsConfig(BaseParameterConfig):
    """
    """
    fide_player_id: FideID = Field(..., alias='id1')
    fide_player_opponent_id: FideIDOptional = Field(..., alias='id2')

    @property
    def parameterize(self) -> Dict[str, Any]:
        """
        """
        return self.model_dump(by_alias=True)
    

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
    

class PlayerOpponentsConfig(BaseParameterConfig):
    """
    """
    fide_player_id: FideID = Field(..., alias='pl')
    
    @property
    def parameterize(self) -> Dict[str, Any]:
        """
        """
        return self.model_dump(by_alias=True)