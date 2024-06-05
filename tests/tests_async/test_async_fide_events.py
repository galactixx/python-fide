from typing import Any, Dict, Union
from unittest import mock
import pytest

from python_fide.clients_async import AsyncFideEventsClient
from python_fide import (
    Date,
    FideEvent,
    FideEventDetail,
    FideEventID,
    InvalidFideIDError
)

from python_fide.parsing.event_parsing import event_detail_parsing
from tests.utils import (
    load_json_file,
    MockedResponse
)

fide_events_client = AsyncFideEventsClient()

FIDE_EVENT_DETAIL_CANDIDATES = FideEventDetail(
    city='Toronto',
    country='Canada',
    start_date=Date.from_date_format(date='2024-04-03 00:00:00', date_format='%Y-%m-%d %H:%M:%S'),
    end_date=Date.from_date_format(date='2024-04-23 23:59:59', date_format='%Y-%m-%d %H:%M:%S'),
    game_format='s',
    tournament_type=None,
    time_control=None,
    time_control_desc=None,
    rounds=None,
    players=None,
    telephone=None,
    website='https://candidates2024.fide.com/',
    organizer=None,
    chief_arbiter=None,
    chief_organizer=None,
    event=FideEvent(name='Candidates Tournament', event_id=53626)
)

FIDE_EVENT_DETAIL_CANDIDATES_WOMEN = FideEventDetail(
    city='Toronto',
    country='Canada',
    start_date=Date.from_date_format(date='2024-04-03 00:00:00', date_format='%Y-%m-%d %H:%M:%S'),
    end_date=Date.from_date_format(date='2024-04-23 23:59:59', date_format='%Y-%m-%d %H:%M:%S'),
    game_format='s',
    tournament_type=None,
    time_control=None,
    time_control_desc=None,
    rounds=None,
    players=None,
    telephone=None,
    website='https://candidates2024.fide.com/',
    organizer=None,
    chief_arbiter=None,
    chief_organizer=None,
    event=FideEvent(name="Women's Candidates Tournament", event_id=53627)
)


def test_async_event_detail_parsing() -> None:
    """Testing the event detail parsing functions."""
    fide_response_one: Dict[str, Any] = load_json_file(filename='fide_event_candidates.json')
    event_detail: FideEventDetail = event_detail_parsing(response=fide_response_one)
    assert event_detail == FIDE_EVENT_DETAIL_CANDIDATES

    fide_response_two: Dict[str, Any] = load_json_file(filename='fide_event_candidates_women.json')
    event_detail: FideEventDetail = event_detail_parsing(response=fide_response_two)
    assert event_detail == FIDE_EVENT_DETAIL_CANDIDATES_WOMEN


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'fide_event', [
        FideEventID(entity_id='53626'),
        FideEventID(entity_id=53626),
        FIDE_EVENT_DETAIL_CANDIDATES.event
    ]
)
@mock.patch(
    target='requests.get',
    side_effect=MockedResponse(filename='fide_event_candidates.json').mock_response,
    autospec=True
)
async def test_async_event_mock_detail_candidates(_, fide_event: Union[FideEvent, FideEventID]) -> None:
    """Testing the event detail functionality for example one."""
    event_detail: FideEventDetail = await fide_events_client.get_event_detail(
        fide_event=fide_event
    )
    assert event_detail == FIDE_EVENT_DETAIL_CANDIDATES


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'fide_event', [
        FideEventID(entity_id='53627'),
        FideEventID(entity_id=53627),
        FIDE_EVENT_DETAIL_CANDIDATES_WOMEN.event
    ]
)
@mock.patch(
    target='requests.get',
    side_effect=MockedResponse(filename='fide_event_candidates_women.json').mock_response, 
    autospec=True
)
async def test_async_event_mock_detail_candidates_women(_, fide_event: Union[FideEvent, FideEventID]) -> None:
    """Testing the event detail functionality for example two."""
    event_detail: FideEventDetail = await fide_events_client.get_event_detail(
        fide_event=fide_event
    )
    assert event_detail == FIDE_EVENT_DETAIL_CANDIDATES_WOMEN


@pytest.mark.parametrize(
    'fide_event_id, error', [
        ('H19JF433', 'invalid Fide ID entered, must be an integer (as str in int type)'),
        ('0023FFH8', 'invalid Fide ID entered, must be an integer (as str in int type)'),
        ('003953322', 'invalid Fide ID entered, cannot start with a zero')
    ]
)
def test_async_event_error_invalid_fide_id(fide_event_id: str, error: str) -> None:
    """Testing the InvalidFideIDError for the FideEventID class."""
    with pytest.raises(InvalidFideIDError) as exc_info:
        _ = FideEventID(entity_id=fide_event_id)
    assert str(exc_info.value) == error