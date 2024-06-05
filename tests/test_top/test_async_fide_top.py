from unittest import mock

import pytest
from python_fide.clients_async import AsyncFideTopPlayersClient

from tests.utils import MockedResponse
from tests.test_top.common_top import (
    CaseTopPlayers,
    fide_top_assertion,
    FIDE_TOP_PARAMETERS
)

fide_top_player_client = AsyncFideTopPlayersClient()

@pytest.mark.asyncio
@pytest.mark.parametrize(
    'test_case', FIDE_TOP_PARAMETERS
)
@mock.patch(
    target='httpx.AsyncClient.get',
    side_effect=MockedResponse(filename='fide_top_players.json').mock_response,
    autospec=True
)
async def test_async_top_players(_, test_case: CaseTopPlayers) -> None:
    """Testing the top ten standard players functionality."""
    top_players = await fide_top_player_client.get_top_ten_standard_rankings(
        limit=test_case.limit, categories=test_case.categories
    )

    fide_top_assertion(test_case=test_case, top_players=top_players)