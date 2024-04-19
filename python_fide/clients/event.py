from typing import List, Optional, Union

from python_fide.clients.base_client import FideClientWithPagination
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

class FideEventsClient(FideClientWithPagination):
    """
    """
    def __init__(self):
        self.base_url = (
            'https://app.fide.com/api/v1/client/events/'
        )
        self.base_latest_url = (
            'https://app.fide.com/api/v1/events/'
        )

    def get_latest_events(
        self,
        limit: Optional[int] = None,
        query: Optional[str] = None
    ) -> List[FideEventDetail]:
        """
        """
        config = EventLatestConfig(limit=limit, query=query)

        pagination = self._paginatize(
            limit=limit,
            base_url=self.base_latest_url,
            config=config,
            fide_type=FideEventDetail
        )

        return pagination.records

    def get_event_detail(
        self,
        fide_event: Union[FideEvent, FideEventID]
    ) -> Optional[FideEventDetail]:
        """
        """
        config = EventDetailConfig.from_event_object(
            fide_event=fide_event
        )

        # Request from API to get profile detail JSON response
        fide_url = config.endpointize(base_url=self.base_url)
        response = self._fide_request(fide_url=fide_url)

        # Validate and parse profile detail fields from response
        player_detail = event_detail_parsing(
            response=response
        )

        # If the ID from the found Fide event does not match the
        # Fide ID passed in as an argument, then return None
        if (
            player_detail is not None and
            player_detail.event.event_id != config.fide_event_id
        ):
            return
        return player_detail