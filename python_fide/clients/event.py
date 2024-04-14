from typing import Union

from python_fide.parsing.event_parsing import event_detail_parsing
from python_fide.config.event_config import EventDetailConfig
from python_fide.clients.base_client import FideClient
from python_fide.types import (
    FideEvent,
    FideEventDetail,
    FideEventID,
)

class FideEvents(FideClient):
    """
    """
    def __init__(self):
        self.base_url = (
            'https://app.fide.com/api/v1/client/events/'
        )

    def get_event_detail(
        self,
        fide_event: Union[FideEvent, FideEventID]
    ) -> FideEventDetail:
        """
        """
        config = EventDetailConfig(fide_event=fide_event)

        # Request from API to get profile detail JSON response
        response = self._fide_request(
            fide_url=config.endpointize(
                base_url=self.base_url
            )
        )

        # Validate and parse profile detail fields from response
        player_detail = event_detail_parsing(
            response=response
        )

        # If the ID from the found Fide event does not match the
        # Fide ID passed in as an argument, then return None
        if (
            player_detail is not None and
            player_detail.event.event_id != config.fide_event
        ):
            return
        return player_detail