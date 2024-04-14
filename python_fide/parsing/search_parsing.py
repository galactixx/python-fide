from typing import Any, Dict, List

from python_fide.types import (
    FideEvent,
    FideNews,
    FidePlayer
)

def search_player_parsing(record: Dict[str, Any]) -> List[FidePlayer]:
    """
    """
    fide_player = FidePlayer.from_validated_model(player=record)
    return fide_player


def search_event_parsing(record: Dict[str, Any]) -> List[FideEvent]:
    """
    """
    fide_event = FideEvent.model_validate(record)
    return fide_event


def search_news_parsing(record: Dict[str, Any]) -> List[FideNews]:
    """
    """
    fide_news = FideNews.model_validate(record)
    return fide_news