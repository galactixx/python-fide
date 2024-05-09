from typing import List, Optional
from unittest import mock
import pytest
from dataclasses import dataclass

from python_fide import (
    FideTopPlayer,
    FideTopPlayersClient,
    RatingCategory
)

from tests.utils import MockedResponse

fide_top_player_client = FideTopPlayersClient()

@dataclass
class CaseTopPlayers:
    limit: Optional[int]
    categories: Optional[List[RatingCategory]]
    exp_girls: int = 0
    exp_open: int = 0
    exp_juniors: int = 0
    exp_women: int = 0


def _category_count(players: List[FideTopPlayer], category: RatingCategory) -> int:
    return sum(
        player.category == category.value for player in players
    )


@pytest.mark.parametrize(
    'test_case', [
        CaseTopPlayers(limit=5, categories=[RatingCategory.GIRLS], exp_girls=5),
        CaseTopPlayers(limit=1, categories=[RatingCategory.OPEN], exp_open=1),
        CaseTopPlayers(limit=8, categories=[RatingCategory.JUNIORS], exp_juniors=8),
        CaseTopPlayers(limit=3, categories=[RatingCategory.WOMEN], exp_women=3),
        CaseTopPlayers(limit=7, categories=[RatingCategory.OPEN, RatingCategory.WOMEN], exp_women=7, exp_open=7),
        CaseTopPlayers(
            limit=2, categories=[RatingCategory.GIRLS, RatingCategory.JUNIORS], exp_girls=2, exp_juniors=2
        ),
        CaseTopPlayers(
            limit=4, categories=[RatingCategory.OPEN, RatingCategory.JUNIORS, RatingCategory.WOMEN], exp_open=4, exp_juniors=4, exp_women=4
        ),
        CaseTopPlayers(
            limit=6, categories=[RatingCategory.GIRLS, RatingCategory.WOMEN], exp_girls=6, exp_women=6
        )
    ]
)
@mock.patch(
    target='requests.get',
    side_effect=MockedResponse(filename='fide_top_players.json').mock_response,
    autospec=True
)
def test_top_players(_, test_case: CaseTopPlayers) -> None:
    """
    """
    top_players = fide_top_player_client.get_top_ten_standard_rankings(
        limit=test_case.limit, categories=test_case.categories
    )

    assert all(
        isinstance(player, FideTopPlayer) for player in top_players
    )

    assert _category_count(players=top_players, category=RatingCategory.GIRLS) == test_case.exp_girls
    assert _category_count(players=top_players, category=RatingCategory.JUNIORS) == test_case.exp_juniors
    assert _category_count(players=top_players, category=RatingCategory.OPEN) == test_case.exp_open
    assert _category_count(players=top_players, category=RatingCategory.WOMEN) == test_case.exp_women
