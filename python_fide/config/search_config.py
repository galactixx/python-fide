from typing import Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator

from python_fide.utils.general import validate_limit
from python_fide.config.base_config import BaseConfig
from python_fide.types import (
    FideEventID,
    FideNewsID,
    FidePlayerID,
    FidePlayerName
)

class PaginationConfig(BaseModel):
    page: int = Field(..., alias='page')


class SearchConfig(BaseConfig):
    query: Union[
        str,
        FideEventID,
        FideNewsID,
        FidePlayerID,
        FidePlayerName
    ] = Field(..., alias='query')
    link: Literal[
        'player',
        'event',
        'news'
    ] = Field(..., alias='link')

    @field_validator('query', mode='after')
    @classmethod
    def extract_query(
        cls, 
        query: Union[
            str,
            FideEventID,
            FideNewsID,
            FidePlayerID,
            FidePlayerName
        ]
    ) -> str:
        if isinstance(query, str):
            return query
        if isinstance(query,
            (FideEventID, FideNewsID, FidePlayerID)
        ):
            return query.entity_id
        elif isinstance(query, FidePlayerName):
            return query.search_name
        else:
            raise TypeError(
                "not a valid search query type"
            )

    @property
    def parameterize(self) -> dict:
        return self.model_dump(by_alias=True)
    
    def parameterize_with_pagination(self, page: int) -> dict:
        pagination_config = PaginationConfig(
            page=page
        )

        return (
            self.model_dump(by_alias=True) |
            pagination_config.model_dump(by_alias=True)
        )
    

class SearchPagination:
    def __init__(self, limit: Optional[int]):
        self._limit = validate_limit(limit=limit)

        # Page tracking variables
        self._current_page = 1
        self._overflow_pages = None

        # Record tracking variables
        self._records_parsed = 0
        self._gathered_records: list = []

    @property
    def loop_continue(self) -> bool:
        return self._records_parsed < self._limit and (
            self._overflow_pages is None or self._current_page <= self._overflow_pages
        )
    
    @property
    def overflow_pages(self) -> Optional[int]:
        return self._overflow_pages
    
    @overflow_pages.setter
    def overflow_pages(self, pages: int) -> None:
        self._overflow_pages = pages

    @property
    def current_page(self) -> int:
        return self._current_page

    @property
    def records(self) -> list:
        return self._gathered_records[:self._limit]

    def update_status(self, records: list) -> None:
        self._gathered_records.extend(records)
        self._records_parsed += len(records)

        # Update current page
        self._current_page += 1