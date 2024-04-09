from typing import Callable, Dict, List, Optional

from python_fide.clients.base_client import BaseClient
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
    FideNews,
    FidePlayer
)

class FideSearchClient(BaseClient):
    """
    """
    def __init__(self):
        super().__init__()

        self.base_url = FIDE_SEARCH_URL
        self.headers: Dict[str, str] = FIDE_HEADERS

    def get_player(
        self,
        first_name: str, 
        last_name: str
    ) -> Optional[FidePlayer]:
        """
        """
        players = self.get_players(
            first_name=first_name, last_name=last_name
        )

        if len(players) == 1:
            return players[0]
        
        return

    def get_players(
        self,
        first_name: str, 
        last_name: str
    ) -> List[FidePlayer]:
        """
        """
        combined_name_query = f'{last_name}, {first_name}'

        # Instantiate configuration for searching players
        config = SearchConfig(
            query=combined_name_query, link='player'
        )

        response_json = self._fide_request(
            fide_url=self.base_url,
            params=config.parameterize,
            headers=self.headers
        )

        players = search_player_parsing(response=response_json)
        return players

    def get_events(
        self,
        query: str, 
        limit: Optional[int] = None
    ) -> List[FideEvent]:
        """
        """
        # Instantiate configuration for searching events
        config = SearchConfig(
            query=query, link='event'
        )

        pagination = self._paginate(
            limit=limit,
            config=config,
            parser=search_event_parsing
        )

        return pagination.records

    def get_news(
        self,
        query: str, 
        limit: Optional[int] = None
    ) -> List[FideNews]:
        """
        """
        # Instantiate configuration for searching news
        config = SearchConfig(
            query=query, link='news'
        )

        pagination = self._paginate(
            limit=limit,
            config=config,
            parser=search_news_parsing
        )

        return pagination.records
    
    def _paginate(
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
                fide_url=self.base_url,
                params=params,
                headers=self.headers
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