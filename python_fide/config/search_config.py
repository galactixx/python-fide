from typing import Any, Deque, Dict, Literal, Union
from collections import deque

from pydantic import Field

from python_fide.utils.general import combine_fide_player_names
from python_fide.config.base_config import BaseParameterConfig
from python_fide.types import (
    FideEventID,
    FideNewsID,
    FidePlayerID,
    FidePlayerName
)

class BaseSearchConfig(BaseParameterConfig):
    link: Literal['event', 'news', 'player']


class SearchConfig(BaseSearchConfig):
    """
    """
    query: Union[str, int]

    @classmethod
    def from_search_object(
        cls,
        link: Literal['event', 'news'],
        query: Union[str, int]
    ) -> 'SearchConfig':
        """
        """
        if isinstance(query, str):
            return cls(query=query, link=link)
        elif isinstance(query, (FideEventID, FideNewsID)):
            return cls(query=query.entity_id, link=link)
        else:
            raise TypeError("not a valid 'query' type")
        
    @property
    def parameterize(self) -> Dict[str, Any]:
        return self.model_dump()


class SearchPlayerNameConfig(BaseSearchConfig):
    """
    """
    fide_player_name: str = Field(..., alias='query')

    def model_post_init(self, __context: Any) -> None:
        self.__num_requests: int = 0

    @classmethod
    def from_player_name_object(
        cls, link: Literal['player'], fide_player_name: FidePlayerName
    ) -> 'SearchPlayerNameConfig':
        """
        """
        return cls(
            link=link, fide_player_name=fide_player_name.last_name,
        )

    def update_player_name(self, fide_player_name: FidePlayerName) -> None:
        """
        """
        first_name_substring = fide_player_name.first_name[:self.__num_requests]
        self.__num_requests += 1

        self.fide_player_name = combine_fide_player_names(
            first_name=first_name_substring, last_name=self.fide_player_name
        )

    @property
    def parameterize(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True)


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
    
    @property
    def parameterize(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True)