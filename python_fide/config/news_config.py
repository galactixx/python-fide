from typing import Optional, Union
import sys

from pydantic import field_validator

from python_fide.utils.general import build_url
from python_fide.config.base_config import (
    BaseEndpointConfig,
    ParameterNullConfig
)
from python_fide.types.core import (
    FideNews,
    FideNewsID
)

class NewsLatestConfig(ParameterNullConfig):
    """
    Simple configuration for the latest news endpoint from the FideNewsClient.

    Args:
        limit (int): An integer of the maximum number of news stories to parse
            and return.
    """
    limit: int

    @field_validator('limit', mode='before')
    @classmethod
    def validate_limit(cls, limit: Optional[int]) -> int:
        """Validation for limit parameter."""
        if limit is None:
            return sys.maxsize
        else:
            assert isinstance(limit, int), 'limit argument has to be an integer'
            assert limit > 0, 'limit argument has to be more than 0'
            return limit


class NewsDetailConfig(BaseEndpointConfig):
    """
    Simple configuration for the news detail endpoint from the FideNewsClient.

    Args:
        fide_news_id (int): An integer representing the Fide ID for a news story.
    """
    fide_news_id: int

    @classmethod
    def from_news_object(
        cls,
        fide_news: Union[FideNews, FideNewsID]
    ) -> 'NewsDetailConfig':
        """
        Create an NewsDetailConfig instance from a FideNews or FideNewsID object.

        Args:
            fide_news (FideNews | FideNewsID): A FideNews or FideNewsID object.
        
        Returns:
            NewsDetailConfig: A new NewsDetailConfig instance.
        """
        if isinstance(fide_news, FideNews):
            return cls(fide_news_id=fide_news.news_id)
        elif isinstance(fide_news, FideNewsID):
            return cls(fide_news_id=fide_news.entity_id)
        else:
            raise ValueError(
                f"{type(fide_news)} not a valid 'fide_news' type"
            )
    
    def endpointize(self, base_url: str) -> str:
        """Build the news detail endpoint."""
        return build_url(
            base=base_url, segments=self.fide_news_id
        )