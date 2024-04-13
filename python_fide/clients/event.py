from typing import Union

from python_fide.clients.fide_client import fide_request
from python_fide.parsing.event_parsing import event_detail_parsing
from python_fide.config.event_config import EventDetailConfig
from python_fide.constants.common import (
    FIDE_EVENTS_DETAIL_URL,
    FIDE_RATINGS_HEADERS
)
from python_fide.types import (
    FideEvent,
    FideEventDetail,
    FideEventID,
    URLInfo
)

def get_event_detail(
    fide_event: Union[FideEvent, FideEventID]
) -> FideEventDetail:
    """
    """
    config = EventDetailConfig(fide_event=fide_event)

    # Request from API to get profile detail JSON response
    response = fide_request(
        url_info=URLInfo(
            url=config.endpointize, headers=FIDE_RATINGS_HEADERS
        )
    )

    # Validate and parse profile detail fields from response
    player_detail = event_detail_parsing(
        response=response
    )

    # If the ID from the found Fide player does not match the
    # Fide ID passed in as an argument, then return None
    if (
        player_detail is not None and
        player_detail.event.event_id != config.fide_event
    ):
        return
    return player_detail