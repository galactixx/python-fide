from typing import Literal, Union

from pydantic import field_validator

from python_fide.config.base_config import BaseParameterConfig
from python_fide.types import (
    FideEventID,
    FideNewsID,
    FidePlayerID,
    FidePlayerName
)

class SearchConfig(BaseParameterConfig):
    """
    """
    query: Union[
        str,
        FideEventID,
        FideNewsID,
        FidePlayerID,
        FidePlayerName
    ]
    link: Literal[
        'player',
        'event',
        'news'
    ]

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
        elif isinstance(query,
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
        return self.model_dump()