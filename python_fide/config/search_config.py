from typing import Any, Deque, Dict, Literal, Union
from collections import deque

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
    

class PlayerIDSearch:
    """
    """
    def __init__(
        self,
        query: int,
        model: 'SearchPlayerConfig'
    ):
        self.model = model
        self._fide_ids_to_parse: Deque[int] = deque([query])

        self.current_id: int = None

    def update_id(self) -> None:
        """
        """
        self.current_id = self._fide_ids_to_parse.popleft()
        self.model.query = self.current_id

    def add_ids(self) -> None:
        """
        """
        self._fide_ids_to_parse.extend(
            int(f'{self.current_id}{integer}') for integer in range(10)
        )

    @property
    def stop_loop(self) -> bool:
        return not self._fide_ids_to_parse


class PlayerNameSearch:
    """
    """
    def __init__(
        self,
        query: str,
        query_type: FidePlayerName,
        model: 'SearchPlayerConfig'
    ):
        self.query = query
        self.query_type = query_type
        self.model = model
        self._num_requests = 0

    def update_name(self) -> None:
        """
        """
        first_name_substring = self.query_type.first_name[:self._num_requests]
        self.model.query = combine_fide_player_names(
            first_name=first_name_substring, last_name=self.query
        )
        self._num_requests += 1


class SearchPlayerConfig(BaseSearchConfig):
    """
    """
    query: Union[FidePlayerID, FidePlayerName]

    def initialize_search_env(
        self,
        query_type: Union[FidePlayerID, FidePlayerName]
    ) -> Union[PlayerIDSearch, PlayerNameSearch]:
        """
        """
        if isinstance(query_type, FidePlayerID):
            return PlayerIDSearch(
                query=self.query, model=self
            )
        else:
            return PlayerNameSearch(
                query=self.query, query_type=query_type, model=self
            )

    @field_validator('query', mode='after')
    @classmethod
    def extract_query(
        cls,
        query: Union[FidePlayerID, FidePlayerName]
    ) -> Union[str, int]:
        """
        """
        if isinstance(query, FidePlayerID):
            return query.entity_id
        elif isinstance(query, FidePlayerName):
            return query.last_name
        else:
            raise TypeError("not a valid 'query' type")