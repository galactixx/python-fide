from typing import Any, Dict, Union

from pydantic import BaseModel, field_validator

from python_fide.utils.config import parse_fide_event
from python_fide.constants.common import FIDE_EVENTS_DETAIL_URL
from python_fide.utils.general import create_url
from python_fide.types import (
    FideEvent, 
    FideEventID
)

class EventDetailConfig(BaseModel):
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
    
    @property
    def endpointize(self) -> str:
        return create_url(
            base=FIDE_EVENTS_DETAIL_URL, segments=str(self.fide_event)
        )