from typing import Union
from unittest import mock

import pytest
from python_fide.clients_async import AsyncFidePlayerClient
from python_fide import (
    FidePlayer,
    FidePlayerDetail,
    FidePlayerID,
    Period
)

from tests.utils import MockedResponse
from tests.test_players.common_players import (
    FIDE_PLAYER_DETAIL_CARLSEN,
    FIDE_PLAYER_DETAIL_NAKAMURA,
    FIDE_PLAYER_PARAMETERS_CARLSEN,
    FIDE_PLAYER_PARAMETERS_NAKAMURA,
    game_stats_assertion,
    opponents_assertion,
    rating_chart_assertion
)

fide_player_client = AsyncFidePlayerClient()

@pytest.mark.asyncio
@pytest.mark.parametrize(
    'fide_player', FIDE_PLAYER_PARAMETERS_CARLSEN
)
@mock.patch(
    target='httpx.AsyncClient.get',
    side_effect=MockedResponse(filename='fide_player_carlsen.json').mock_response,
    autospec=True
)
async def test_async_player_mock_detail_carlsen(
    _, fide_player: Union[FidePlayer, FidePlayerID]
) -> None:
    """Testing the player detail functionality for example one."""
    player_detail: FidePlayerDetail = await fide_player_client.get_fide_player_detail(
        fide_player=fide_player
    )
    assert player_detail == FIDE_PLAYER_DETAIL_CARLSEN


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'fide_player', FIDE_PLAYER_PARAMETERS_NAKAMURA
)
@mock.patch(
    target='httpx.AsyncClient.get',
    side_effect=MockedResponse(filename='fide_player_nakamura.json').mock_response,
    autospec=True
)
async def test_async_player_mock_detail_nakamura(
    _, fide_player: Union[FidePlayer, FidePlayerID]
) -> None:
    """Testing the player detail functionality for example two."""
    player_detail: FidePlayerDetail = await fide_player_client.get_fide_player_detail(
        fide_player=fide_player
    )
    assert player_detail == FIDE_PLAYER_DETAIL_NAKAMURA


@pytest.mark.asyncio
@mock.patch(
    target='httpx.AsyncClient.get',
    side_effect=MockedResponse(filename='fide_opponents.json').mock_response,
    autospec=True
)
async def test_async_player_mock_opponents(_) -> None:
    """Testing the player opponents functionality."""
    opponents = await fide_player_client.get_fide_player_opponents(
        fide_player=FIDE_PLAYER_DETAIL_CARLSEN.player
    )

    opponents_assertion(opponents=opponents)


@pytest.mark.asyncio
@mock.patch(
    target='httpx.AsyncClient.get',
    side_effect=MockedResponse(filename='fide_rating_chart.json').mock_response,
    autospec=True
)
async def test_async_player_mock_rating_progress_chart(_) -> None:
    """Testing the player historical ratings functionality."""
    historical_ratings = await fide_player_client.get_fide_player_rating_progress_chart(
        period=Period.ONE_YEAR, fide_player=FIDE_PLAYER_DETAIL_CARLSEN.player
    )

    rating_chart_assertion(historical_ratings=historical_ratings)


@pytest.mark.asyncio
@mock.patch(
    target='httpx.AsyncClient.get',
    side_effect=MockedResponse(filename='fide_game_stats.json').mock_response,
    autospec=True
)
async def test_async_player_mock_game_stats(_) -> None:
    """Testing the player game statistics functionality."""
    game_stats = await fide_player_client.get_fide_player_game_stats(
        fide_player=FIDE_PLAYER_DETAIL_CARLSEN.player
    )

    game_stats_assertion(game_stats=game_stats)