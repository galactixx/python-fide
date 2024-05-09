from typing import Optional, Union
import sys

from pydantic import field_validator

from python_fide.utils.general import build_url
from python_fide.config.base_config import (
    BaseEndpointConfig,
    ParameterNullConfig
)
from python_fide.types.core import (
    FideEvent,
    FideEventID
)

class EventLatestConfig(ParameterNullConfig):
    """
    Simple configuration for the latest events endpoint from the FideEventsClient.

    Args:
        limit (int): An integer of the maximum number of events to parse
            and return.
    """
    limit: int

    @field_validator('limit', mode='before')
    @classmethod
    def validate_limit(cls, limit: Optional[int]) -> int:
        """Validation for limit parameter."""
        if limit is None:
            return sys.maxsize
        else:
            assert isinstance(limit, int), 'limit argument has to be an integer'
            assert limit > 0, 'limit argument has to be more than 0'
            return limit


class EventDetailConfig(BaseEndpointConfig):
    """
    Simple configuration for the event detail endpoint from the FideEventsClient.

    Args:
        fide_event_id (int): An integer representing the Fide ID for an event.
    """
    fide_event_id: int

    @classmethod
    def from_event_object(
        cls,
        fide_event: Union[FideEvent, FideEventID]
    ) -> 'EventDetailConfig':
        """
        Create an EventDetailConfig instance from a FideEvent or FideEventID object.

        Args:
            fide_event (FideEvent | FideEventID): A FideEvent or FideEventID object.
        
        Returns:
            EventDetailConfig: A new EventDetailConfig instance.
        """
        if isinstance(fide_event, FideEvent):
            return cls(fide_event_id=fide_event.event_id)
        elif isinstance(fide_event, FideEventID):
            return cls(fide_event_id=fide_event.entity_id)
        else:
            raise ValueError(
                f"{type(fide_event)} not a valid 'fide_event' type"
            )
    
    def endpointize(self, base_url: str) -> str:
        """Build the events detail endpoint."""
        return build_url(
            base=base_url, segments=self.fide_event_id
        )