from typing import Union
from unittest import mock

import pytest
from python_fide.clients_async import AsyncFideEventsClient
from python_fide import (
    FideEvent,
    FideEventDetail,
    FideEventID
)

from tests.utils import MockedResponse
from tests.test_events.common_events import (
    FIDE_EVENT_DETAIL_CANDIDATES,
    FIDE_EVENT_DETAIL_CANDIDATES_WOMEN,
    FIDE_EVENT_PARAMETERS_CANDIDATES,
    FIDE_EVENT_PARAMETERS_CANDIDATES_WOMEN
)

fide_events_client = AsyncFideEventsClient()

@pytest.mark.asyncio
@pytest.mark.parametrize(
    'fide_event', FIDE_EVENT_PARAMETERS_CANDIDATES
)
@mock.patch(
    target='httpx.AsyncClient.get',
    side_effect=MockedResponse(filename='fide_event_candidates.json').mock_response,
    autospec=True
)
async def test_async_event_mock_detail_candidates(
    _, fide_event: Union[FideEvent, FideEventID]
) -> None:
    """Testing the event detail functionality for example one."""
    event_detail: FideEventDetail = await fide_events_client.get_event_detail(
        fide_event=fide_event
    )
    assert event_detail == FIDE_EVENT_DETAIL_CANDIDATES


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'fide_event', FIDE_EVENT_PARAMETERS_CANDIDATES_WOMEN
)
@mock.patch(
    target='httpx.AsyncClient.get',
    side_effect=MockedResponse(filename='fide_event_candidates_women.json').mock_response, 
    autospec=True
)
async def test_async_event_mock_detail_candidates_women(
    _, fide_event: Union[FideEvent, FideEventID]
) -> None:
    """Testing the event detail functionality for example two."""
    event_detail: FideEventDetail = await fide_events_client.get_event_detail(
        fide_event=fide_event
    )
    assert event_detail == FIDE_EVENT_DETAIL_CANDIDATES_WOMEN