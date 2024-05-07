from typing import Any, Dict, Union
from unittest import mock
import pytest

from python_fide import (
    Date,
    FideEvent,
    FideEventDetail,
    FideEventID,
    FideEventsClient,
    InvalidFideIDError
)

from python_fide.parsing.event_parsing import event_detail_parsing
from tests.utils import (
    load_json_file,
    mock_request
)

fide_events_client = FideEventsClient()

FIDE_EVENT_CANDIDATES = FideEvent(name='Candidates Tournament', event_id=53626)
FIDE_EVENT_CANDIDATES_WOMEN = FideEvent(name="Women's Candidates Tournament", event_id=53627)

def _mock_request_event_candidates(*args, **kwargs):
    response = load_json_file(filename='fide_event_candidates.json')
    return mock_request(response=response)


def _mock_request_event_candidates_women(*args, **kwargs):
    response = load_json_file(filename='fide_event_candidates_women.json')
    return mock_request(response=response)


def _assert_event_candidates(event_detail: FideEventDetail) -> None:
    """
    """
    assert event_detail.event == FIDE_EVENT_CANDIDATES
    assert event_detail.city == 'Toronto'
    assert event_detail.country == 'Canada'
    
    assert event_detail.game_format == 's'
    assert event_detail.tournament_type == None
    assert event_detail.time_control == None
    assert event_detail.time_control_desc == None
    assert event_detail.rounds == None
    assert event_detail.players == None
    assert event_detail.telephone == None
    assert event_detail.website == 'https://candidates2024.fide.com/'
    assert event_detail.organizer == None
    assert event_detail.chief_arbiter == None
    assert event_detail.chief_organizer == None
    assert event_detail.start_date == Date(
        date_iso='2024-04-03', date_original='2024-04-03 00:00:00', date_original_format='%Y-%m-%d %H:%M:%S'
    )
    assert event_detail.end_date == Date(
        date_iso='2024-04-23', date_original='2024-04-23 23:59:59', date_original_format='%Y-%m-%d %H:%M:%S'
    )


def _assert_event_candidates_women(event_detail: FideEventDetail) -> None:
    """
    """
    assert event_detail.event == FIDE_EVENT_CANDIDATES_WOMEN
    assert event_detail.city == 'Toronto'
    assert event_detail.country == 'Canada'
    
    assert event_detail.game_format == 's'
    assert event_detail.tournament_type == None
    assert event_detail.time_control == None
    assert event_detail.time_control_desc == None
    assert event_detail.rounds == None
    assert event_detail.players == None
    assert event_detail.telephone == None
    assert event_detail.website == 'https://candidates2024.fide.com/'
    assert event_detail.organizer == None
    assert event_detail.chief_arbiter == None
    assert event_detail.chief_organizer == None
    assert event_detail.start_date == Date(
        date_iso='2024-04-03', date_original='2024-04-03 00:00:00', date_original_format='%Y-%m-%d %H:%M:%S'
    )
    assert event_detail.end_date == Date(
        date_iso='2024-04-23', date_original='2024-04-23 23:59:59', date_original_format='%Y-%m-%d %H:%M:%S'
    )


def test_event_detail_parsing() -> None:
    """
    """
    fide_response_one: Dict[str, Any] = load_json_file(filename='fide_event_candidates.json')
    event_detail: FideEventDetail = event_detail_parsing(response=fide_response_one)
    _assert_event_candidates(event_detail=event_detail)

    fide_response_two: Dict[str, Any] = load_json_file(filename='fide_event_candidates_women.json')
    event_detail: FideEventDetail = event_detail_parsing(response=fide_response_two)
    _assert_event_candidates_women(event_detail=event_detail)


@pytest.mark.parametrize(
    'fide_event', [
        FideEventID(entity_id='53626'),
        FideEventID(entity_id=53626),
        FIDE_EVENT_CANDIDATES
    ]
)
@mock.patch(
    'requests.get', side_effect=_mock_request_event_candidates, autospec=True
)
def test_event_mock_detail_candidates(_, fide_event: Union[FideEvent, FideEventID]) -> None:
    """
    """
    event_detail: FideEventDetail = fide_events_client.get_event_detail(
        fide_event=fide_event
    )
    _assert_event_candidates(event_detail=event_detail)


@pytest.mark.parametrize(
    'fide_event', [
        FideEventID(entity_id='53627'),
        FideEventID(entity_id=53627),
        FIDE_EVENT_CANDIDATES_WOMEN
    ]
)
@mock.patch(
    'requests.get', side_effect=_mock_request_event_candidates_women, autospec=True
)
def test_event_mock_detail_candidates_women(_, fide_event: Union[FideEvent, FideEventID]) -> None:
    """
    """
    event_detail: FideEventDetail = fide_events_client.get_event_detail(
        fide_event=fide_event
    )
    _assert_event_candidates_women(event_detail=event_detail)


@pytest.mark.parametrize(
    'fide_event_id, error', [
        ('H19JF433', 'invalid Fide ID entered, must be an integer (as str in int type)'),
        ('0023FFH8', 'invalid Fide ID entered, must be an integer (as str in int type)'),
        ('003953322', 'invalid Fide ID entered, cannot start with a zero')
    ]
)
def test_event_error_invalid_fide_id(fide_event_id: str, error: str) -> None:
    """
    """
    with pytest.raises(InvalidFideIDError) as exc_info:
        _ = FideEventID(entity_id=fide_event_id)
    assert str(exc_info.value) == error