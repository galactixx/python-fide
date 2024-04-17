from typing import Any, Dict, List

from python_fide.types_adapter import PartialAdapter
from python_fide.types import (
    FideEvent,
    FideNews,
    FidePlayer
)

def search_player_parsing(response: Dict[str, Any]) -> List[FidePlayer]:
    """
    """
    players = PartialAdapter.model_validate(response)
    gathered_players: List[FidePlayer] = []
    
    for player in players.data:
        fide_player = FidePlayer.from_validated_model(player=player)
        gathered_players.append(fide_player)
    
    return gathered_players


def search_event_parsing(record: Dict[str, Any]) -> FideEvent:
    """
    """
    fide_event = FideEvent.model_validate(record)
    return fide_event


def search_news_parsing(record: Dict[str, Any]) -> FideNews:
    """
    """
    fide_news = FideNews.model_validate(record)
    return fide_news