from typing import Any, Deque, Literal, Union
from collections import deque

from pydantic import Field

from python_fide.utils.general import combine_fide_player_names
from python_fide.config.base_config import ParameterAliasConfig
from python_fide.types.core import (
    FideEventID,
    FideNewsID,
    FidePlayerID,
    FidePlayerName
)

class BaseSearchConfig(ParameterAliasConfig):
    """
    Base search configuration for all search endpoints from the FideSearchClient.

    Args:
        link (Literal['event', 'news', 'player']): A literal for the type of search. A
            search can either be by event, news, or player.
    """
    link: Literal['event', 'news', 'player']


class SearchConfig(BaseSearchConfig):
    """
    The search configuration for both the event and news search endpoints from
    the FideSearchClient.

    Args:
        search_query (str | int): A string or integer representing the search query.
    """
    search_query: Union[str, int] = Field(..., alias='query')

    @classmethod
    def from_search_object(
        cls,
        link: Literal['event', 'news'],
        search_query: Union[str, FideEventID, FideNewsID]
    ) -> 'SearchConfig':
        """
        Create a SearchConfig instance from a string, FideEventID or FideNewsID object.

        Args:
            link (Literal['event', 'news']): A literal for the type of search. A
                search can either be by event or news.
            search_query (str | FideEventID | FideNewsID): A string, FideEventID or
                FideNewsID object.
        
        Returns:
            SearchConfig: A new SearchConfig instance.
        """
        if isinstance(search_query, str):
            return cls(search_query=search_query, link=link)
        elif isinstance(search_query, (FideEventID, FideNewsID)):
            return cls(
                search_query=search_query.entity_id, link=link
            )
        else:
            raise TypeError(f"{type(search_query)} not a valid 'query' type")


class SearchPlayerNameConfig(BaseSearchConfig):
    """
    The player name search configuration for the player search endpoint from the
    FideSearchClient. This configuration is used when executing a player search
    by the player name (first and last names).

    Args:
        fide_player_name (str): A string representatin of the name of the player.
        fide_player_type (FidePlayerName): A FidePlayerName object representing the
            name of the player.
    """
    fide_player_name: str = Field(..., alias='query')
    fide_player_type: FidePlayerName = Field(..., exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.__num_requests: int = 0

    @classmethod
    def from_player_name_object(
        cls, link: Literal['player'], fide_player_name: FidePlayerName
    ) -> 'SearchPlayerNameConfig':
        """
        Create a SearchPlayerNameConfig instance from a FidePlayerName object.

        Args:
            link (Literal['player']): A literal for the type of search.
            fide_player_name (FidePlayerName): A FidePlayerName object representing the
                name of the player.

        Returns:
            SearchPlayerNameConfig: A new SearchPlayerNameConfig instance.
        """
        return cls(
            link=link,
            fide_player_name=fide_player_name.last_name,
            fide_player_type=fide_player_name
        )

    def update_player_name(self) -> None:
        """
        Updates player name used in pagination after each additional request.
        """
        first_name_substring = (
            self.fide_player_type.first_name[:self.__num_requests]
        )
        self.__num_requests += 1

        self.fide_player_name = combine_fide_player_names(
            first_name=first_name_substring,
            last_name=self.fide_player_type.last_name
        )


class SearchPlayerIDConfig(BaseSearchConfig):
    """
    The player ID search configuration for the player search endpoint from the
    FideSearchClient. This configuration is used when executing a player search
    by the player Fide ID.

    Args:
        fide_player_id (int): An integer representing the Fide ID for a player.
    """
    fide_player_id: int = Field(..., alias='query')

    def model_post_init(self, __context: Any) -> None:
        self.__fide_ids_to_parse: Deque[int] = deque([self.fide_player_id])

    def update_player_id(self) -> None:
        """
        Updates the current Fide player ID by popping the next ID the queue
        containing all Fide IDs to iterate through.
        """
        self.fide_player_id = self.__fide_ids_to_parse.popleft()

    def add_player_ids(self) -> None:
        """
        Extends the queue by ten additional Fide player IDs to iterate through.
        """
        self.__fide_ids_to_parse.extend(
            int(f'{self.fide_player_id}{integer}') for integer in range(10)
        )

    @property
    def stop_loop(self) -> bool:
        """The loop control for the pagination."""
        return not self.__fide_ids_to_parse

    @classmethod
    def from_player_id_object(
        cls, link: Literal['player'], fide_player_id: FidePlayerID
    ) -> 'SearchPlayerIDConfig':
        """
        Create a SearchPlayerIDConfig instance from a FidePlayerID object.

        Args:
            link (Literal['player']): A literal for the type of search.
            fide_player_id (FidePlayerID): A FidePlayerID object representing the
                Fide ID of the player.

        Returns:
            SearchPlayerIDConfig: A new SearchPlayerIDConfig instance.
        """
        return cls(
            link=link, fide_player_id=fide_player_id.entity_id
        )