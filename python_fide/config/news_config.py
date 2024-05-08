from typing import Optional, Union

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
    limit: Optional[int]


class NewsDetailConfig(BaseEndpointConfig):
    """
    """
    fide_news_id: int

    @classmethod
    def from_news_object(
        cls,
        fide_news: Union[FideNews, FideNewsID]
    ) -> 'NewsDetailConfig':
        """
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
        return build_url(
            base=base_url, segments=self.fide_news_id
        )