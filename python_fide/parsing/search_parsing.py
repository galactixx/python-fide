from typing import Any, Dict, List

from python_fide.types.adapters import PartialListAdapter
from python_fide.types.core import (
    FideEvent,
    FideNews,
    FidePlayer
)

def search_player_parsing(
    response: Dict[str, Any],
    gathered_players: List[FidePlayer]
) -> List[FidePlayer]:
    """
    """
    players = PartialListAdapter.model_validate(response)
    parsed_players: List[FidePlayer] = []
    
    for player in players.data:
        fide_player = FidePlayer.from_validated_model(player=player)

        if fide_player not in gathered_players:
            parsed_players.append(fide_player)
    
    return parsed_players


def search_event_parsing(record: Dict[str, Any]) -> FideEvent:
    """
    """
    return FideEvent.model_validate(record)


def search_news_parsing(record: Dict[str, Any]) -> FideNews:
    """
    """
    return FideNews.model_validate(record)