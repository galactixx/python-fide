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
    link: Literal['event', 'news', 'player']


class SearchConfig(BaseSearchConfig):
    """
    """
    search_query: Union[str, int] = Field(..., alias='query')

    @classmethod
    def from_search_object(
        cls,
        link: Literal['event', 'news'],
        search_query: Union[str, FideEventID, FideNewsID]
    ) -> 'SearchConfig':
        """
        """
        if isinstance(search_query, str):
            return cls(search_query=search_query, link=link)
        elif isinstance(search_query, (FideEventID, FideNewsID)):
            return cls(
                search_query=search_query.entity_id, link=link
            )
        else:
            raise TypeError("not a valid 'query' type")


class SearchPlayerNameConfig(BaseSearchConfig):
    """
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
        """
        return cls(
            link=link,
            fide_player_name=fide_player_name.last_name,
            fide_player_type=fide_player_name
        )

    def update_player_name(self) -> None:
        """
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
    """
    fide_player_id: int = Field(..., alias='query')

    def model_post_init(self, __context: Any) -> None:
        self.__fide_ids_to_parse: Deque[int] = deque([self.fide_player_id])

    def update_player_id(self) -> None:
        """
        """
        self.fide_player_id = self.__fide_ids_to_parse.popleft()

    def add_player_ids(self) -> None:
        """
        """
        self.__fide_ids_to_parse.extend(
            int(f'{self.fide_player_id}{integer}') for integer in range(10)
        )

    @property
    def stop_loop(self) -> bool:
        """
        """
        return not self.__fide_ids_to_parse

    @classmethod
    def from_player_id_object(
        cls, link: Literal['player'], fide_player_id: FidePlayerID
    ) -> 'SearchPlayerIDConfig':
        """
        """
        return cls(
            link=link, fide_player_id=fide_player_id.entity_id
        )