from typing import List, Optional, Union

from python_fide.clients.base_client import FideClient
from python_fide.parsing.news_parsing import (
    news_detail_parsing,
    news_latest_parsing
)
from python_fide.config.news_config import (
    NewsDetailConfig,
    NewsLatestConfig
)
from python_fide.types import (
    FideNews,
    FideNewsDetail,
    FideNewsID
)

class FideNews(FideClient):
    """
    """
    def __init__(self):
        self.base_url = (
            'https://app.fide.com/api/v1/client/news/'
        )

    def get_latest_news(
        self,
        limit: Optional[int] = None,
        query: Optional[str] = None
    ) -> List[FideNews]:
        """
        """
        config = NewsLatestConfig(limit=limit, query=query)

        pagination = self._paginatize(
            limit=limit,
            base_url=self.base_url,
            config=config,
            parser=news_latest_parsing
        )

        return pagination.records

    def get_news_detail(
        self,
        fide_news: Union[FideNews, FideNewsID]
    ) -> FideNewsDetail:
        """
        """
        config = NewsDetailConfig.from_news_object(
            fide_news=fide_news
        )

        # Request from API to get profile detail JSON response
        response = self._fide_request(
            fide_url=config.endpointize(
                base_url=self.base_url
            )
        )

        # Validate and parse profile detail fields from response
        player_detail = news_detail_parsing(
            response=response
        )

        # If the ID from the found Fide news does not match the
        # Fide ID passed in as an argument, then return None
        if (
            player_detail is not None and
            player_detail.news.news_id != config.fide_news
        ):
            return
        return player_detail