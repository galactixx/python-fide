from typing import Callable, List, Optional, Union

from python_fide.pagination.core_paginate import SearchPagination
from python_fide.config.search_config import SearchConfig
from python_fide.clients.base_client import FideClient
from python_fide.types import (
    FideEvent, 
    FideEventID,
    FidePlayerName,
    FideNews,
    FideNewsID,
    FidePlayer,
    FidePlayerID
)
from python_fide.parsing.search_parsing import (
    search_event_parsing,
    search_news_parsing,
    search_player_parsing,
    search_result_pages
)

class FideSearch(FideClient):
    """
    """
    def __init__(self):
        self.base_url = (
            'https://app.fide.com/api/v1/client/search?'
        )

    def get_events(
        self,
        query: Union[str, FideEventID, FidePlayerName], 
        limit: Optional[int] = None
    ) -> List[FideEvent]:
        """
        """
        config = SearchConfig(
            query=query, link='event'
        )

        pagination = self._paginatize(
            limit=limit, config=config, parser=search_event_parsing
        )

        return pagination.records
    
    def get_news_search(
        self,
        query: Union[str, FideNewsID, FidePlayerName], 
        limit: Optional[int] = None
    ) -> List[FideNews]:
        """
        """
        config = SearchConfig(
            query=query, link='news'
        )

        pagination = self._paginatize(
            limit=limit, config=config, parser=search_news_parsing
        )

        return pagination.records
    
    def get_fide_player_profiles(
        self,
        query: Union[FidePlayerID, FidePlayerName]
    ) -> List[FidePlayer]:
        """
        """
        config = SearchConfig(
            query=query, link='player'
        )

        response_json = self._fide_request(
            fide_url=self.base_url, params=config.parameterize
        )

        players = search_player_parsing(
            response=response_json
        )
        return players
    
    def get_fide_player_profile(
        self,
        query: Union[FidePlayerID, FidePlayerName]
    ) -> Optional[FidePlayer]:
        """
        """
        players = self.get_fide_player_profiles(query=query)

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
                "not a valid 'query' type"
            )
        return
    
    def _paginatize(
        self,
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

            response_json = self._fide_request(
                fide_url=self.base_url, params=params
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