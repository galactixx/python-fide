from unittest import mock
from typing import Any

import pytest

from python_fide import FidePlayerID, Period
from python_fide.clients_async import AsyncFidePlayerClient
from tests.common import (
    game_stats_assertion,
    opponents_assertion,
    rating_chart_assertion,
)
from tests.utils import MockedResponse

fide_player_client = AsyncFidePlayerClient()


@pytest.mark.asyncio
@mock.patch(
    target="httpx.AsyncClient.get",
    side_effect=MockedResponse(filename="fide_opponents.json").mock_response,
    autospec=True,
)
async def test_async_player_mock_opponents(_: Any) -> None:
    """Testing the player opponents functionality."""
    opponents = await fide_player_client.get_opponents(
        fide_player=FidePlayerID(fide_id=1503014)
    )
    opponents_assertion(opponents=opponents)


@pytest.mark.asyncio
@mock.patch(
    target="httpx.AsyncClient.get",
    side_effect=MockedResponse(filename="fide_rating_chart.json").mock_response,
    autospec=True,
)
async def test_async_player_mock_rating_progress_chart(_: Any) -> None:
    """Testing the player historical ratings functionality."""
    historical_ratings = await fide_player_client.get_rating_progress_chart(
        period=Period.ONE_YEAR, fide_id=FidePlayerID(fide_id=1503014)
    )
    rating_chart_assertion(historical_ratings=historical_ratings)


@pytest.mark.asyncio
@mock.patch(
    target="httpx.AsyncClient.get",
    side_effect=MockedResponse(filename="fide_game_stats.json").mock_response,
    autospec=True,
)
async def test_async_player_mock_game_stats(_: Any) -> None:
    """Testing the player game statistics functionality."""
    game_stats = await fide_player_client.get_game_stats(
        fide_id=FidePlayerID(fide_id=1503014)
    )
    game_stats_assertion(game_stats=game_stats)
