from typing import Any, Dict, List

from python_fide.types.core import FideTopPlayer
from python_fide.enums import RatingCategory
from python_fide.types.adapters import TopPlayersAdapter

def top_standard_players_parsing(
    limit: int,
    response: Dict[str, Any],
    categories: List[RatingCategory]
) -> List[FideTopPlayer]:
    """
    """
    top_categories = TopPlayersAdapter.model_validate(response)
    gathered_players: List[FideTopPlayer] = []

    for category in categories:
        player_count = 0
        players = iter(getattr(top_categories, category.value))

        while player_count < limit:
            try:
                player = next(players)
                fide_player = FideTopPlayer.from_validated_model(
                    player=player,
                    category=category
                )

                gathered_players.append(fide_player)
                player_count += 1
            except StopIteration:
                break

    return gathered_players