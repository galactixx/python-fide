from typing import Union

from python_fide.types import (
    FideEvent,
    FideEventID,
    FideNews,
    FideNewsID,
    FidePlayer,
    FidePlayerID
)

def parse_fide_player(
    fide_player: Union[FidePlayer, FidePlayerID]
) -> str:
    """
    """
    if isinstance(fide_player, FidePlayer):
        return fide_player.player_id
    elif isinstance(fide_player, FidePlayerID):
        return fide_player.entity_id
    else:
        raise ValueError(
            "not a valid 'fide_player' type"
        )
    

def parse_fide_event(
    fide_event: Union[FideEvent, FideEventID]
) -> str:
    """
    """
    if isinstance(fide_event, FideEvent):
        return fide_event.event_id
    elif isinstance(fide_event, FideEventID):
        return fide_event.entity_id
    else:
        raise ValueError(
            "not a valid 'fide_event' type"
        )
    

def parse_fide_news(
    fide_news: Union[FideNews, FideNewsID]
) -> str:
    """
    """
    if isinstance(fide_news, FideNews):
        return fide_news.news_id
    elif isinstance(fide_news, FideNewsID):
        return fide_news.entity_id
    else:
        raise ValueError(
            "not a valid 'fide_news' type"
        )