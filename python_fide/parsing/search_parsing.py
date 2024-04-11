from typing import Dict, List

from python_fide.types import (
    FideEvent,
    FideNews,
    FidePlayer
)

def search_result_pages(response: dict) -> int:
    return response['meta']['last_page']


def search_player_parsing(response: dict) -> List[FidePlayer]:
    gathered_players: List[FidePlayer] = []
    players: List[Dict[str, str]] = response['data']

    for player in players:
        fide_player = FidePlayer.from_validated_model(player)
        gathered_players.append(fide_player)

    return gathered_players


def search_event_parsing(response: dict) -> List[FideEvent]:
    gathered_events: List[FideEvent] = []
    events: List[Dict[str, str]] = response['data']

    for event in events:
        fide_event = FideEvent.model_validate(event)
        gathered_events.append(fide_event)

    return gathered_events


def search_news_parsing(response: dict) -> List[FideNews]:
    gathered_news_stories: List[FideNews] = []
    news_stories: List[Dict[str, str]] = response['data']

    for news_story in news_stories:
        fide_news = FideNews.model_validate(news_story)
        gathered_news_stories.append(fide_news)

    return gathered_news_stories