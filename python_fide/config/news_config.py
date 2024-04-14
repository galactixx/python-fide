from typing import Any, Dict, Optional, Union

from pydantic import field_validator

from python_fide.utils.config import parse_fide_news
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
    fide_news: Union[
        FideNews, FideNewsID
    ]

    @field_validator('fide_news', mode='after')
    @classmethod
    def extract_fide_id(
        cls,
        fide_news: Union[FideNews, FideNewsID]
    ) -> str:
        news_id = parse_fide_news(fide_news=fide_news)
        return news_id
    
    def endpointize(self, base_url: str) -> str:
        return create_url(
            base=base_url, segments=self.fide_news
        )
    

class NewsLatestConfig(BaseParameterConfig):
    limit: Optional[int]
    query: Optional[str]

    @property
    def parameterize(self) -> Dict[str, Any]:
        return dict()