from typing import Optional

from pydantic import Field, field_validator
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

from python_fide._enums import RatingPeriod
from python_fide.config._base import BaseEndpointConfig
from python_fide.utils._config import parse_fide_player, parse_fide_player_optional

FideID = Annotated[int, BeforeValidator(parse_fide_player)]
FideIDOptional = Annotated[Optional[int], BeforeValidator(parse_fide_player_optional)]


class PlayerOpponentsConfig(BaseEndpointConfig):
    """
    Simple configuration for the opponents endpoint.
    """

    fide_id: FideID = Field(..., alias="pl")


class PlayerChartsConfig(BaseEndpointConfig):
    """
    Simple configuration for the ratings charts endpoint.
    """

    fide_id: FideID = Field(..., alias="event")
    period: RatingPeriod = Field(..., alias="period")

    @field_validator("period", mode="before")
    @classmethod
    def validate_period(cls, period: Optional[RatingPeriod]) -> RatingPeriod:
        """Validation for period parameter."""
        if period is None:
            return RatingPeriod.ALL_YEARS
        else:
            return period


class PlayerStatsConfig(BaseEndpointConfig):
    """
    Simple configuration for the game stats endpoint.
    """

    fide_id: FideID = Field(..., alias="id1")
    fide_id_opponent: FideIDOptional = Field(default=None, alias="id2")
