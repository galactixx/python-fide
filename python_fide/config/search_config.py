from typing import Literal, Union

from pydantic import BaseModel, Field, field_validator

from python_fide.config.base_config import BaseConfig
from python_fide.types import (
    FideEventID,
    FideNewsID,
    FidePlayerID,
    FidePlayerName
)

class PaginationConfig(BaseModel):
    """
    """
    page: int = Field(..., alias='page')


class SearchConfig(BaseConfig):
    """
    """
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