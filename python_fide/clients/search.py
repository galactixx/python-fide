from typing import List, Optional, Union

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
    search_player_parsing
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
            limit=limit,
            base_url=self.base_url,
            config=config,
            parser=search_event_parsing
        )

        return pagination.records
    
    def get_news(
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
            limit=limit,
            base_url=self.base_url,
            config=config,
            parser=search_news_parsing
        )

        return pagination.records
    
    def get_fide_players(
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
    
    def get_fide_player(
        self,
        query: Union[FidePlayerID, FidePlayerName]
    ) -> Optional[FidePlayer]:
        """
        """
        players = self.get_fide_players(query=query)

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
            raise TypeError("not a valid 'query' type")
        return