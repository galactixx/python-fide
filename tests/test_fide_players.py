from typing import Any, Dict
from unittest import mock
import pytest

from python_fide import (
    FidePlayer,
    FidePlayerClient,
    FidePlayerDetail,
    FidePlayerID,
    InvalidFideIDError
)

from python_fide.parsing.player_parsing import player_detail_parsing
from tests.utils import (
    load_json_file,
    mock_request
)
from tests.examples.parameters.player_parameters import (
    FIDE_PLAYER_DETAIL_1503014,
    FIDE_PLAYER_DETAIL_2016192
)

fide_player_client = FidePlayerClient()

def _mock_request_news_1503014(*args, **kwargs):
    response = load_json_file(filename='fide_player_1503014.json')
    return mock_request(response=response)


def _mock_request_news_2016192(*args, **kwargs):
    response = load_json_file(filename='fide_player_2016192.json')
    return mock_request(response=response)


def test_player_detail_parsing() -> None:
    """
    """
    fide_response_one: Dict[str, Any] = load_json_file(filename='fide_player_1503014.json')
    event_detail: FidePlayerDetail = player_detail_parsing(response=fide_response_one)
    assert event_detail.birth_year == FIDE_PLAYER_DETAIL_1503014.birth_year
    assert event_detail.sex == FIDE_PLAYER_DETAIL_1503014.sex
    assert event_detail.player == FIDE_PLAYER_DETAIL_1503014.player

    fide_response_one: Dict[str, Any] = load_json_file(filename='fide_player_2016192.json')
    event_detail: FidePlayerDetail = player_detail_parsing(response=fide_response_one)
    assert event_detail.birth_year == FIDE_PLAYER_DETAIL_2016192.birth_year
    assert event_detail.sex == FIDE_PLAYER_DETAIL_2016192.sex
    assert event_detail.player == FIDE_PLAYER_DETAIL_2016192.player


@mock.patch(
    'requests.get', side_effect=_mock_request_news_1503014, autospec=True
)
def test_player_mock_detail_1503014(_) -> None:
    """
    """
    player_detail: FidePlayerDetail = fide_player_client.get_fide_player_detail(
        fide_player=FidePlayerID(entity_id='1503014')
    )
    assert player_detail == FIDE_PLAYER_DETAIL_1503014

    player_detail: FidePlayerDetail = fide_player_client.get_fide_player_detail(
        fide_player=FidePlayerID(entity_id=1503014)
    )
    assert player_detail == FIDE_PLAYER_DETAIL_1503014

    player_detail: FidePlayerDetail = fide_player_client.get_fide_player_detail(
        fide_player=FidePlayer(
            name='Magnus Carlsen',
            player_id=1503014,
            title='GM',
            country='NOR',
            first_name='Magnus',
            last_name='Carlsen'
        )
    )
    assert player_detail == FIDE_PLAYER_DETAIL_1503014


@mock.patch(
    'requests.get', side_effect=_mock_request_news_2016192, autospec=True
)
def test_player_mock_detail_2016192(_) -> None:
    """
    """
    player_detail: FidePlayerDetail = fide_player_client.get_fide_player_detail(
        fide_player=FidePlayerID(entity_id='2016192')
    )
    assert player_detail == FIDE_PLAYER_DETAIL_2016192

    player_detail: FidePlayerDetail = fide_player_client.get_fide_player_detail(
        fide_player=FidePlayerID(entity_id=2016192)
    )
    assert player_detail == FIDE_PLAYER_DETAIL_2016192

    player_detail: FidePlayerDetail = fide_player_client.get_fide_player_detail(
        fide_player=FidePlayer(
            name='Hikaru Nakamura',
            player_id=2016192,
            title='GM',
            country='USA',
            first_name='Hikaru',
            last_name='Nakamura'
        )
    )
    assert player_detail == FIDE_PLAYER_DETAIL_2016192


@mock.patch(
    'requests.get', side_effect='', autospec=True
)
def test_player_mock_opponents(_) -> None:
    """
    """
    pass


@mock.patch(
    'requests.get', side_effect='', autospec=True
)
def test_player_mock_rating_progress_chart(_) -> None:
    """
    """
    pass


@mock.patch(
    'requests.get', side_effect='', autospec=True
)
def test_player_mock_game_stats(_) -> None:
    """
    """
    pass


def test_player_error_invalid_fide_id() -> None:
    """
    """
    with pytest.raises(InvalidFideIDError) as exc_info:
        _ = FidePlayerID(entity_id='H19JF433')
    assert str(exc_info.value) == 'invalid Fide ID entered, must be an integer (as str in int type)'

    with pytest.raises(InvalidFideIDError) as exc_info:
        _ = FidePlayerID(entity_id='0023FFH8')
    assert str(exc_info.value) == 'invalid Fide ID entered, must be an integer (as str in int type)'

    with pytest.raises(InvalidFideIDError) as exc_info:
        _ = FidePlayerID(entity_id='003953322')
    assert str(exc_info.value) == 'invalid Fide ID entered, cannot start with a zero'