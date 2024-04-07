from typing import Dict, List

from python_fide.types import (
    Event,
    News,
    Player
)

def search_player_parsing(response: dict) -> List[Player]:
    gathered_players: List[Player] = []
    players: List[Dict[str, str]] = response['data']

    for player in players:
        player_name = player['name'].split(',')
        player_first_name = player_name[0].strip()
        player_last_name = ' '.join(
            name.strip() for name in player_name[1:]
        )

        gathered_players.append(
            Player(
                first_name=player_first_name,
                last_name=player_last_name,
                player_id=player['id'], 
                title=player['title'],
                country=player['country']
            )
        )
    return gathered_players


def search_result_pages(response: dict) -> int:
    return response['meta']['last_page']


def search_event_parsing(response: dict) -> List[Event]:
    gathered_events: List[Player] = []
    events: List[Dict[str, str]] = response['data']

    for event in events:
        gathered_events.append(
            Event(
                name=event['name'], event_id=str(event['id'])
            )
        )
    return gathered_events


def search_news_parsing(response: dict) -> List[News]:
    gathered_news_stories: List[News] = []
    news_stories: List[Dict[str, str]] = response['data']

    for news in news_stories:
        gathered_news_stories.append(
            News(
                title=news['name'], news_id=str(news['id'])
            )
        )
    return gathered_news_stories