from typing import List
from unittest import mock

import pytest
from python_fide.clients_async import AsyncFideSearchClient
from python_fide import (
    FideEvent,
    FideNewsBasic,
    FidePlayer,
    FidePlayerID,
    FidePlayerName
)

from tests.utils import MockedResponse

fide_search_client = AsyncFideSearchClient()

@pytest.mark.asyncio
@mock.patch(
    target="httpx.AsyncClient.get",
    side_effect=MockedResponse(filename='fide_search_events.json').mock_response,
    autospec=True
)
async def test_async_event_mock_search(_) -> None:
    """Testing the event search functionality."""
    fide_events: List[FideEvent] = await fide_search_client.get_events(query='Chess', limit=4)

    assert len(fide_events) == 4
    assert all(isinstance(event, FideEvent) for event in fide_events)


@pytest.mark.asyncio
@mock.patch(
    target="httpx.AsyncClient.get",
    side_effect=MockedResponse(filename='fide_search_news.json').mock_response,
    autospec=True
)
async def test_async_news_mock_search(_) -> None:
    """Testing the news search functionality."""
    fide_news: List[FideNewsBasic] = await fide_search_client.get_news(query='Chess', limit=6)

    assert len(fide_news) == 6
    assert all(isinstance(event, FideNewsBasic) for event in fide_news)


@pytest.mark.asyncio
@mock.patch(
    target="httpx.AsyncClient.get",
    side_effect=MockedResponse(filename='fide_search_players.json').mock_response,
    autospec=True
)
async def test_async_player_mock_search(_) -> None:
    """Testing the player search functionality."""
    fide_players: List[FidePlayer] = await fide_search_client.get_fide_players_by_name(
        fide_player_name=FidePlayerName(first_name='Hikaru', last_name='Nakamura')
    )

    assert len(fide_players) == 1
    assert all(isinstance(event, FidePlayer) for event in fide_players)

    fide_players: List[FidePlayer] = await fide_search_client.get_fide_players_by_id(
        fide_player_id=FidePlayerID(entity_id=2016192)
    )

    assert len(fide_players) == 1
    assert all(isinstance(event, FidePlayer) for event in fide_players)