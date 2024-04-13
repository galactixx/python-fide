from typing import Any, Dict, List

from python_fide.types import FideTopPlayer
from python_fide.constants.rating_cat import RatingCategory

def top_standard_players_parsing(
    limit: int,
    response: Dict[str, Any],
    categories: List[RatingCategory]
) -> List[FideTopPlayer]:
    """
    """
    gathered_players: List[FideTopPlayer] = []

    for category in categories:
        player_count = 0
        players = iter(response[category.value])

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