from typing import Callable, List, Optional, Union

from python_fide.clients.fide_client import FideClient
from python_fide.constants.common import (
    FIDE_HEADERS,
    FIDE_SEARCH_URL
)
from python_fide.endpoint.search_endpoint import (
    SearchConfig,
    SearchPagination
)
from python_fide.parsing.search_parsing import (
    search_event_parsing,
    search_news_parsing,
    search_player_parsing,
    search_result_pages,
)
from python_fide.types import (
    FideEvent,
    FideEventID,
    FideNews,
    FideNewsID,
    FidePlayer,
    FidePlayerID,
    FidePlayerName,
    URLInfo
)

FIDE_SEARCH_INFO = URLInfo(
    url=FIDE_SEARCH_URL, headers=FIDE_HEADERS
)

def get_fide_player(
    query: Union[FidePlayerID, FidePlayerName]
) -> Optional[FidePlayer]:
    """
    """
    players = get_fide_players(query=query)

    if isinstance(query, FidePlayerID):
        player_gen = (
            player for player in players
            if query.entity_id == player.player_id
        )
        return next(player_gen, None)
    elif isinstance(query, FidePlayerName):
        if len(players) == 1:
            return players[0]
    else:
        raise TypeError(
            "not a valid search query type"
        )

    return


def get_fide_players(
    query: Union[FidePlayerID, FidePlayerName]
) -> List[FidePlayer]:
    """
    """
    with FideClient() as session:
        config = SearchConfig(
            query=query, link='player'
        )

        response_json = session.request(
            params=config.parameterize,
            url_info=FIDE_SEARCH_INFO
        )

        players = search_player_parsing(
            response=response_json
        )
        return players


def get_fide_news(
    query: Union[str, FideNewsID, FidePlayerName], 
    limit: Optional[int] = None
) -> List[FideNews]:
    """
    """
    with FideClient() as session:
        config = SearchConfig(
            query=query, link='news'
        )

        pagination = _paginate(
            session=session,
            limit=limit,
            config=config,
            parser=search_news_parsing
        )

        return pagination.records


def get_fide_events(
    query: Union[str, FideEventID, FidePlayerName], 
    limit: Optional[int] = None
) -> List[FideEvent]:
    """
    """
    with FideClient() as session:
        config = SearchConfig(
            query=query, link='event'
        )

        pagination = _paginate(
            session=session,
            limit=limit,
            config=config,
            parser=search_event_parsing
        )

        return pagination.records


def _paginate(
    session: FideClient,
    limit: Optional[int],
    config: SearchConfig,
    parser: Callable[[dict], list]
) -> SearchPagination:
    """
    """
    search_pagination = SearchPagination(
        limit=limit
    )

    while search_pagination.loop_continue:
        params = config.parameterize_with_pagination(
            page=search_pagination.current_page
        )

        response_json = session.request(
            params=params,
            url_info=FIDE_SEARCH_INFO
        )

        if search_pagination.overflow_pages is None:
            search_pagination.overflow_pages = search_result_pages(
                response=response_json
            )

        # Parse and gather all news from response
        records = parser(response=response_json)

        # Update all record and page variables
        # (both dataclasses to be returned and number of these
        # records that have been parsed)
        search_pagination.update_status(
            records=records
        )

    return search_pagination