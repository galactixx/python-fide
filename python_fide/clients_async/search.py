from typing import List, Optional, Union

from python_fide.clients_async.base_client import AsyncFideClientPaginate
from python_fide.parsing.search_parsing import search_player_parsing
from python_fide.config.search_config import (
    SearchConfig,
    SearchPlayerIDConfig,
    SearchPlayerNameConfig
)
from python_fide.types.core import (
    FideEvent, 
    FideEventID,
    FidePlayerName,
    FideNewsBasic,
    FideNewsID,
    FidePlayer,
    FidePlayerID
)

# The maximum results returned from the player search endpoint
_MAX_RESULTS_PLAYER = 300

class AsyncFideSearchClient(AsyncFideClientPaginate):
    """
    A Fide search client which provides methods to perform a lexical search
    through all players, events, and news.
    """
    def __init__(self):
        self.base_url = 'https://app.fide.com/api/v1/client/search?'

    async def get_events(
        self,
        query: Union[str, FideEventID], 
        limit: Optional[int] = None
    ) -> List[FideEvent]:
        """
        Given a query, being a string or FideEventID object, will return a list
        of FideEvent objects that represent events associated with the query.

        Args:
            query (str | FideEventID): A string query or FideEventID object.
            limit (int | None): An integer of the maximum number of events to parse
                and return.

        Returns:
            List[FideEvent]: A list of FideEvent objects.
        """
        config = SearchConfig.from_search_object(
            search_query=query, link='event'
        )

        pagination = await self._paginatize(
            limit=limit,
            fide_url=self.base_url,
            config=config,
            fide_type=FideEvent
        )

        return pagination.records
    
    async def get_news(
        self,
        query: Union[str, FideNewsID], 
        limit: Optional[int] = None
    ) -> List[FideNewsBasic]:
        """
        Given a query, being a string or FideNewsID object, will return a list
        of FideNewsBasic objects that represent news associated associated with
        the query. A FideNewsBasic object is a mariginally less detailed version
        of the FideNews object.

        Args:
            query (str | FideNewsID): A string query or FideNewsID object.
            limit (int | None): An integer of the maximum number of news stories
                to parse and return.

        Returns:
            List[FideNewsBasic]: A list of FideNewsBasic objects.
        """
        config = SearchConfig.from_search_object(
            search_query=query, link='news'
        )

        pagination = await self._paginatize(
            limit=limit,
            fide_url=self.base_url, 
            config=config,
            fide_type=FideNewsBasic
        )

        return pagination.records
    
    async def get_fide_players_by_id(
        self,
        fide_player_id: FidePlayerID
    ) -> List[FidePlayer]:
        """
        Given a FidePlayerID object, will return all Fide players whose Fide ID
        starts with the ID passed. For example, if 'FidePlayerID(entityid=1503014)'
        is passed, then a list of only one FidePlayer will be returned since this
        ID corresponds to a single player. On the other hand, if 'FidePlayerID(entityid=150)'
        is passed, then a list of FidePlayers will be returned, corresponding with all
        players whose Fide ID starts with 150. 
        
        Args:
            fide_player_id (FidePlayerID): A FidePlayerID object, containing the Fide ID.

        Returns:
            List[FidePlayer]: A list of FidePlayer objects.
        """
        config = SearchPlayerIDConfig.from_player_id_object(
            fide_player_id=fide_player_id, link='player'
        )

        gathered_players: List[FidePlayer] = []
        while not config.stop_loop:
            config.update_player_id()

            response_json = await self._fide_request_wrapped(
                fide_url=self.base_url, params=config.parameterize
            )
            if response_json is None:
                continue

            # Validate and parse player fields from response
            players = search_player_parsing(
                response=response_json, gathered_players=gathered_players
            )            
            gathered_players.extend(players)

            # If there is an overflow of players for a Fide ID, then
            # add all possible next Fide IDs to the queue
            if len(players) == _MAX_RESULTS_PLAYER:
                config.add_player_ids()

        return gathered_players
    
    async def get_fide_players_by_name(
        self,
        fide_player_name: FidePlayerName
    ) -> List[FidePlayer]:
        """
        Given a FidePlayerName object, will return all Fide players whose name
        matches the first/last name passed.
        
        Args:
            fide_player_name (FidePlayerName): A FidePlayerName object containing
                the first and last name of the player.

        Returns:
            List[FidePlayer]: A list of FidePlayer objects.
        """
        config = SearchPlayerNameConfig.from_player_name_object(
            fide_player_name=fide_player_name, link='player'
        )

        gathered_players: List[FidePlayer] = []
        while True:
            response_json = await self._fide_request_wrapped(
                fide_url=self.base_url, params=config.parameterize
            )

            if response_json is None:
                return gathered_players

            # Validate and parse player fields from response
            players = search_player_parsing(
                response=response_json, gathered_players=gathered_players
            )
            gathered_players.extend(players)

            # If there is not an overflow of players for a Fide ID, then
            # break out of loop and return parsed player objects
            if len(players) < _MAX_RESULTS_PLAYER:
                break

            config.update_player_name()

        gathered_players_filtered = [
            player for player in gathered_players if (
                player.first_name == fide_player_name.first_name and
                player.last_name == fide_player_name.last_name
            )
        ]
        return gathered_players_filtered
    
    async def get_fide_player(
        self,
        query: Union[FidePlayerID, FidePlayerName]
    ) -> Optional[FidePlayer]:
        """
        Given a FidePlayerID or FidePlayerName object, will return a singular
        FidePlayer object only if a match could be found based on Fide ID, or
        there was only one player found through the search. If neither are true,
        then None is returned.
                
        Args:
            query (FidePlayerID | FidePlayerName): A FidePlayerID or FidePlayerName object.

        Returns:
            List[FidePlayer]: A list of FidePlayer objects.
        """
        if isinstance(query, FidePlayerID):
            players = await self.get_fide_players_by_id(fide_player_id=query)
        elif isinstance(query, FidePlayerName):
            players = await self.get_fide_players_by_name(fide_player_name=query)
        else:
            raise TypeError(f"{type(query)} not a valid 'query' type")

        # If query is a FidePlayerID instance, function only
        # returns a FidePlayer object if a Fide ID can be matched
        # exactly with one from the FidePlayerID instance
        if isinstance(query, FidePlayerID):
            return next(
                (player for player in players if player.player_id == query.entity_id), None
            )
        
        # If query is a FidePlayerName instance, function only
        # returns a FidePlayer object if there was one player
        # returned from 'get_fide_players' call
        else:
            if len(players) == 1:
                return players[0]

        # If a singular Fide player could not be found, function
        # returns None
        return