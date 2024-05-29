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
    Simple configuration for the opponents endpoint from
    the FidePlayerClient.

    Args:
        fide_player_id (FideID): An integer representing
            the Fide ID for a player.
    """
    fide_player_id: FideID = Field(..., alias='pl')


class PlayerChartsConfig(ParameterAliasConfig):
    """
    Simple configuration for the ratings charts endpoint
    from the FidePlayerClient.

    Args:
        fide_player_id (FideID): An integer representing
            the Fide ID for a player.
        period (Period): An enum which allows filtering of
            the ratings data by period of time.
    """
    fide_player_id: FideID = Field(..., alias='event')
    period: Period = Field(..., alias='period')

    @field_validator('period', mode='before')
    @classmethod
    def validate_period(cls, period: Optional[Period]) -> Period:
        """Validation for period parameter."""
        if period is None:
            return Period.ALL_YEARS
        else:
            return period


class PlayerStatsConfig(ParameterAliasConfig):
    """
    Simple configuration for the game stats endpoint from
    the FidePlayerClient.

    Args:
        fide_player_id (FideID): An integer representing the
            Fide ID for a player.
        fide_player_opponent (FideIDOptional): An integer
            representing the Fide ID for a player. Can also
            be None if the entire game history should be returned.
    """
    fide_player_id: FideID = Field(..., alias='id1')
    fide_player_opponent_id: FideIDOptional = Field(default=None, alias='id2')
    

class PlayerDetailConfig(BaseEndpointConfig):
    """
    Simple configuration for the player detail endpoint
    from the FidePlayerClient.

    Args:
        fide_player_id (FideID): An integer representing
            the Fide ID for a player.
    """
    fide_player_id: FideID
    
    def endpointize(self, base_url: str) -> str:
        """Build the player detail endpoint."""
        return build_url(
            base=base_url, segments=self.fide_player_id
        )