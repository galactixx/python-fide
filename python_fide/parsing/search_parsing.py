from typing import Any, Dict, List

from python_fide.types.adapters import PartialListAdapter
from python_fide.types.core import FidePlayer

def search_player_parsing(
    response: Dict[str, Any],
    gathered_players: List[FidePlayer]
) -> List[FidePlayer]:
    """
    Logic to parse the response returned from the search
    player endpoint.

    Args:
        response (Dict[str, Any]): A dictionary representation
            of the JSON response.
        gathered_players (List[FidePlayer]): A list of all players
            that have already been parsed. This is important if
            multiple pages of results are being iterated through,
            where there is risk of duplicate players.

    Returns:
        List[FidePlayer]: A list of FidePlayer objects.
    """
    players = PartialListAdapter.model_validate(response)
    parsed_players: List[FidePlayer] = []
    
    for player in players.data:
        fide_player = FidePlayer.from_validated_model(player=player)

        if fide_player not in gathered_players:
            parsed_players.append(fide_player)
    
    return parsed_players