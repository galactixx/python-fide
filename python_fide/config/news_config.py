from typing import Union

from pydantic import BaseModel, field_validator

from python_fide.utils.config import parse_fide_news
from python_fide.utils.general import create_url
from python_fide.types import (
    FideNews,
    FideNewsID
)

class NewsDetailConfig(BaseModel):
    """
    """
    fide_news: Union[
        FideNews, 
        FideNewsID
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