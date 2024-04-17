from typing import Any, Dict, Optional, Union

from python_fide.utils.general import create_url
from python_fide.config.base_config import (
    BaseEndpointConfig,
    BaseParameterConfig
)
from python_fide.types import (
    FideNews,
    FideNewsID
)

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
                "not a valid 'fide_news' type"
            )
    
    def endpointize(self, base_url: str) -> str:
        return create_url(
            base=base_url, segments=self.fide_news_id
        )
    

class NewsLatestConfig(BaseParameterConfig):
    limit: Optional[int]
    query: Optional[str]

    @property
    def parameterize(self) -> Dict[str, Any]:
        return dict()