from typing import Any, Dict
from unittest import mock
import pytest

from python_fide import (
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
from tests.examples.parameters.event_parameters import (
    FIDE_EVENT_DETAIL_53626,
    FIDE_EVENT_DETAIL_53627
)

fide_events_client = FideEventsClient()

def _mock_request_event_53626(*args, **kwargs):
    response = load_json_file(filename='fide_event_53626.json')
    return mock_request(response=response)


def _mock_request_event_53627(*args, **kwargs):
    response = load_json_file(filename='fide_event_53627.json')
    return mock_request(response=response)


def test_event_detail_parsing() -> None:
    """
    """
    fide_response_one: Dict[str, Any] = load_json_file(filename='fide_event_53626.json')
    event_detail: FideEventDetail = event_detail_parsing(response=fide_response_one)
    assert event_detail == FIDE_EVENT_DETAIL_53626

    fide_response_two: Dict[str, Any] = load_json_file(filename='fide_event_53627.json')
    event_detail: FideEventDetail = event_detail_parsing(response=fide_response_two)
    assert event_detail == FIDE_EVENT_DETAIL_53627


@mock.patch(
    'requests.get', side_effect=_mock_request_event_53626, autospec=True
)
def test_event_mock_detail_53626(_) -> None:
    """
    """
    event_detail: FideEventDetail = fide_events_client.get_event_detail(
        fide_event=FideEventID(entity_id='53626')
    )
    assert event_detail == FIDE_EVENT_DETAIL_53626

    event_detail: FideEventDetail = fide_events_client.get_event_detail(
        fide_event=FideEventID(entity_id=53626)
    )
    assert event_detail == FIDE_EVENT_DETAIL_53626

    event_detail: FideEventDetail = fide_events_client.get_event_detail(
        fide_event=FideEvent(name='Candidates Tournament', event_id=53626)
    )
    assert event_detail == FIDE_EVENT_DETAIL_53626


@mock.patch(
    'requests.get', side_effect=_mock_request_event_53627, autospec=True
)
def test_event_mock_detail_53627(_) -> None:
    """
    """
    event_detail: FideEventDetail = fide_events_client.get_event_detail(
        fide_event=FideEventID(entity_id='53627')
    )
    assert event_detail == FIDE_EVENT_DETAIL_53627

    event_detail: FideEventDetail = fide_events_client.get_event_detail(
        fide_event=FideEventID(entity_id=53627)
    )
    assert event_detail == FIDE_EVENT_DETAIL_53627

    event_detail: FideEventDetail = fide_events_client.get_event_detail(
        fide_event=FideEvent(name="Women's Candidates Tournament", event_id=53627)
    )
    assert event_detail == FIDE_EVENT_DETAIL_53627


def test_event_error_invalid_fide_id() -> None:
    """
    """
    with pytest.raises(InvalidFideIDError) as exc_info:
        _ = FideEventID(entity_id='H19JF433')
    assert str(exc_info.value) == 'invalid Fide ID entered, must be an integer (as str in int type)'

    with pytest.raises(InvalidFideIDError) as exc_info:
        _ = FideEventID(entity_id='0023FFH8')
    assert str(exc_info.value) == 'invalid Fide ID entered, must be an integer (as str in int type)'

    with pytest.raises(InvalidFideIDError) as exc_info:
        _ = FideEventID(entity_id='003953322')
    assert str(exc_info.value) == 'invalid Fide ID entered, cannot start with a zero'