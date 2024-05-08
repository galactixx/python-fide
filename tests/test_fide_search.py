from typing import List
from unittest import mock

from python_fide import (
    FideEvent,
    FideNewsBasic,
    FidePlayer,
    FidePlayerID,
    FidePlayerName,
    FideSearchClient
)

from tests.utils import MockedResponse

fide_search_client = FideSearchClient()

@mock.patch(
    target="requests.get",
    side_effect=MockedResponse(filename='fide_search_events.json').mock_response,
    autospec=True
)
def test_event_mock_search(_) -> None:
    """
    """
    fide_events: List[FideEvent] = fide_search_client.get_events(query='Chess', limit=4)

    assert len(fide_events) == 4
    assert all(isinstance(event, FideEvent) for event in fide_events)


@mock.patch(
    target="requests.get",
    side_effect=MockedResponse(filename='fide_search_news.json').mock_response,
    autospec=True
)
def test_news_mock_search(_) -> None:
    """
    """
    fide_news: List[FideNewsBasic] = fide_search_client.get_news(query='Chess', limit=6)

    assert len(fide_news) == 6
    assert all(isinstance(event, FideNewsBasic) for event in fide_news)


@mock.patch(
    target="requests.get",
    side_effect=MockedResponse(filename='fide_search_players.json').mock_response,
    autospec=True
)
def test_player_mock_search(_) -> None:
    """
    """
    fide_players: List[FidePlayer] = fide_search_client.get_fide_players_by_name(
        fide_player_name=FidePlayerName(first_name='Hikaru', last_name='Nakamura')
    )

    assert len(fide_players) == 1
    assert all(isinstance(event, FidePlayer) for event in fide_players)

    fide_players: List[FidePlayer] = fide_search_client.get_fide_players_by_id(
        fide_player_id=FidePlayerID(entity_id=2016192)
    )

    assert len(fide_players) == 1
    assert all(isinstance(event, FidePlayer) for event in fide_players)