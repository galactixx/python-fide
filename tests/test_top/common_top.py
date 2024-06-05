from dataclasses import dataclass
from typing import (
    List,
    Optional
)

from python_fide import (
    FideTopPlayer,
    RatingCategory
)

@dataclass
class CaseTopPlayers:
    limit: Optional[int]
    categories: Optional[List[RatingCategory]]
    exp_girls: int = 0
    exp_open: int = 0
    exp_juniors: int = 0
    exp_women: int = 0


def __category_count(players: List[FideTopPlayer], category: RatingCategory) -> int:
    return sum(
        player.category == category.value for player in players
    )


def fide_top_assertion(
    test_case: CaseTopPlayers, top_players: List[FideTopPlayer]
) -> None:
    """"""
    assert all(
        isinstance(player, FideTopPlayer) for player in top_players
    )

    assert __category_count(players=top_players, category=RatingCategory.GIRLS) == test_case.exp_girls
    assert __category_count(players=top_players, category=RatingCategory.JUNIORS) == test_case.exp_juniors
    assert __category_count(players=top_players, category=RatingCategory.OPEN) == test_case.exp_open
    assert __category_count(players=top_players, category=RatingCategory.WOMEN) == test_case.exp_women


FIDE_TOP_PARAMETERS = [
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