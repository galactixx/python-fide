from typing import Union

from pydantic import BaseModel, field_validator

from python_fide.utils.config import parse_fide_event
from python_fide.utils.general import create_url
from python_fide.types import (
    FideEvent,
    FideEventID
)

class EventDetailConfig(BaseModel):
    """
    """
    fide_event: Union[
        FideEvent, 
        FideEventID
    ]

    @field_validator('fide_event', mode='after')
    @classmethod
    def extract_fide_id(
        cls,
        fide_event: Union[FideEvent, FideEventID]
    ) -> str:
        news_id = parse_fide_event(fide_event=fide_event)
        return news_id
    
    def endpointize(self, base_url: str) -> str:
        return create_url(
            base=base_url, segments=self.fide_event
        )