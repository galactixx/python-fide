from typing import List, Optional, Union

from python_fide.clients_sync.base_client import FideClientPaginate
from python_fide.parsing.event_parsing import event_detail_parsing
from python_fide.types.core import (
    FideEvent,
    FideEventDetail,
    FideEventID,
)
from python_fide.config.event_config import (
    EventDetailConfig,
    EventLatestConfig
)

class FideEventsClient(FideClientPaginate):
    """
    A Fide events client to pull all event specific
    data from the Fide API. Will pull data for the
    latest events as well as detail for a specific event.
    """
    def __init__(self):
        self.base_url = 'https://app.fide.com/api/v1/client/events/'
        self.base_latest_url = 'https://app.fide.com/api/v1/events/'

    def get_latest_events(
        self,
        limit: Optional[int] = None
    ) -> List[FideEventDetail]:
        """
        Will return all latest events up to a specific
        limit. If no limit is provided then a limit of
        'sys.maxsize' will automatically be set. 

        Args:
            limit (int | None): An integer of the maximum
                number of events to parse and return.
        
        Returns:
            List[FideEventDetail]: A list of FideEventDetail objects.
        """
        config = EventLatestConfig(limit=limit)

        pagination = self._paginatize(
            limit=limit,
            fide_url=self.base_latest_url,
            config=config,
            fide_type=FideEventDetail
        )

        return pagination.records

    def get_event_detail(
        self,
        fide_event: Union[FideEvent, FideEventID]
    ) -> Optional[FideEventDetail]:
        """
        Given a FideEvent or FideEventID object, will
        return a FideEventDetail object containing further
        detail for a Fide event. If the ID included does
        not link to a valid Fide event ID, then None is
        returned.
        
        Args:
            fide_event (FideEvent | FideEventID): A FideEvent
                or FideEventID object.
        
        Returns:
            FideEventDetail | None: A FideEventDetail object
                or if the Fide event ID is invalid, None.
        """
        config = EventDetailConfig.from_event_object(fide_event=fide_event)

        # Request from API to get profile detail JSON response
        fide_url = config.endpointize(base_url=self.base_url)
        response = self._fide_request(fide_url=fide_url)

        # Validate and parse profile detail fields from response
        player_detail = event_detail_parsing(response=response)

        # If the ID from the found Fide event does not match the
        # Fide ID passed in as an argument, then return None
        if (
            player_detail is not None and
            player_detail.event.event_id != config.fide_event_id
        ):
            return
        return player_detail