from typing import List, Optional, Union

from python_fide.clients.base_client import FideClient
from python_fide.config.search_config import (
    SearchConfig,
    SearchPlayerIDConfig,
    SearchPlayerNameConfig
)
from python_fide.types.core import (
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

_MAX_RESULTS_PLAYER = 300

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
        config = SearchConfig.from_search_object(
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
        config = SearchConfig.from_search_object(
            query=query, link='news'
        )

        pagination = self._paginatize(
            limit=limit,
            base_url=self.base_url,
            config=config,
            parser=search_news_parsing
        )

        return pagination.records
    
    def get_fide_players_by_id(
        self,
        fide_player_id: FidePlayerID
    ) -> List[FidePlayer]:
        """
        """
        config = SearchPlayerIDConfig.from_player_id_object(
            fide_player_id=fide_player_id, link='player'
        )

        gathered_players: List[FidePlayer] = []
        while not config.stop_loop:
            config.update_player_id()

            response_json = self._fide_request_wrapped(
                fide_url=self.base_url, params=config.parameterize
            )
            if response_json is None:
                continue

            # Validate and parse player fields from response
            players = search_player_parsing(
                response=response_json,
                gathered_players=gathered_players
            )            
            gathered_players.extend(players)

            # If there is an overflow of players for a Fide ID, then
            # add all possible next Fide IDs to the queue
            if len(players) == _MAX_RESULTS_PLAYER:
                config.add_player_ids()

        return gathered_players
    
    def get_fide_players_by_name(
        self,
        fide_player_name: FidePlayerName
    ) -> List[FidePlayer]:
        """
        """
        config = SearchPlayerNameConfig.from_player_name_object(
            fide_player_name=fide_player_name, link='player'
        )

        gathered_players: List[FidePlayer] = []
        while True:
            response_json = self._fide_request_wrapped(
                fide_url=self.base_url, params=config.parameterize
            )

            if response_json is None:
                return gathered_players

            # Validate and parse player fields from response
            players = search_player_parsing(
                response=response_json,
                gathered_players=gathered_players
            )
            gathered_players.extend(players)

            # If there is not an overflow of players for a Fide ID, then
            # break out of loop and return parsed player objects
            if len(players) < _MAX_RESULTS_PLAYER:
                break

            config.update_player_name()

        gathered_players_filtered = [
            player for player in gathered_players if player == fide_player_name
        ]
        return gathered_players_filtered
    
    def get_fide_player(
        self,
        query: Union[FidePlayerID, FidePlayerName]
    ) -> Optional[FidePlayer]:
        """
        """
        if isinstance(query, FidePlayerID):
            players = self.get_fide_players_by_id(
                fide_player_id=query
            )
        elif isinstance(query, FidePlayerID):
            players = self.get_fide_players_by_name(
                fide_player_name=query
            )
        else:
            raise TypeError("not a valid 'query' type")

        # If query is a FidePlayerID instance, function only returns
        # a FidePlayer object if a Fide ID can be matched exactly with one
        # from the FidePlayerID instance
        if isinstance(query, FidePlayerID):
            return next(
                (
                    player for player in players if player == query
                ), None
            )
        
        # If query is a FidePlayerName instance, function only returns
        # a FidePlayer object if there was one player returned from
        # 'get_fide_players' call
        else:
            if len(players) == 1:
                return players[0]

        # If a singular Fide player could not be found, function
        # returns None
        return