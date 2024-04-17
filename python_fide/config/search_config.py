from typing import Any, Deque, Dict, Literal, Union
from collections import deque
from abc import ABC, abstractmethod

from pydantic import field_validator

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

    @property
    def parameterize(self) -> Dict[str, Any]:
        return self.model_dump()


class SearchConfig(BaseSearchConfig):
    """
    """
    query: Union[str, FideEventID, FideNewsID]

    @field_validator('query', mode='after')
    @classmethod
    def extract_query(
        cls,
        query: Union[str, FideEventID, FideNewsID]
    ) -> str:
        if isinstance(query, str):
            return query
        elif isinstance(query, (FideEventID, FideNewsID)):
            return query.entity_id
        else:
            raise TypeError("not a valid 'query' type")
    

class BaseSearch(ABC):
    @abstractmethod
    def update_query(self) -> Union[int, str]:
        pass


class PlayerIDSearch(BaseSearch):
    """
    """
    def __init__(self, query: FidePlayerID):
        self._fide_ids_to_parse: Deque[int] = deque([query.entity_id])
        self.current_id: int = None

    def update_query(self) -> int:
        """
        """
        self.current_id = self._fide_ids_to_parse.popleft()
        return self.current_id

    def add_ids(self) -> None:
        """
        """
        self._fide_ids_to_parse.extend(
            int(f'{self.current_id}{integer}') for integer in range(10)
        )

    @property
    def stop_loop(self) -> bool:
        return not self._fide_ids_to_parse


class PlayerNameSearch(BaseSearch):
    """
    """
    def __init__(self, query: FidePlayerName):
        self.query = query
        self._num_requests = 0

    def update_query(self) -> str:
        """
        """
        first_name_substring = self.query.first_name[:self._num_requests]
        self._num_requests += 1

        updated_query = combine_fide_player_names(
            first_name=first_name_substring, last_name=self.query.last_name
        )
        return updated_query


class SearchPlayerConfig(BaseSearchConfig):
    """
    """
    query: Union[FidePlayerID, FidePlayerName]

    def initialize_search(self) -> Union[PlayerIDSearch, PlayerNameSearch]:
        """
        """
        if isinstance(self.query, FidePlayerID):
            return PlayerIDSearch(query=self.query)
        else:
            return PlayerNameSearch(query=self.query)

    def update_query(
        self,
        search: Union[PlayerIDSearch, PlayerNameSearch]
    ) -> None:
        """
        """
        self.query = search.update_query()