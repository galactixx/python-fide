from typing import Optional, Union

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
    limit: Optional[int]
    query: Optional[str]


class EventDetailConfig(BaseEndpointConfig):
    """
    """
    fide_event_id: int

    @classmethod
    def from_event_object(
        cls,
        fide_event: Union[FideEvent, FideEventID]
    ) -> 'EventDetailConfig':
        """
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
        return build_url(
            base=base_url, segments=self.fide_event_id
        )