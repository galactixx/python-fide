from typing import Any, Dict, Optional, Union

from python_fide.utils.general import create_url
from python_fide.config.base_config import (
    BaseEndpointConfig,
    BaseParameterConfig
)
from python_fide.types import (
    FideEvent,
    FideEventID
)

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
                "not a valid 'fide_event' type"
            )
    
    def endpointize(self, base_url: str) -> str:
        return create_url(
            base=base_url, segments=self.fide_event_id
        )
    

class EventLatestConfig(BaseParameterConfig):
    limit: Optional[int]
    query: Optional[str]

    @property
    def parameterize(self) -> Dict[str, Any]:
        return dict()