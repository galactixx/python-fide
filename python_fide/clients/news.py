from typing import List, Optional, Union

from python_fide.clients.base_client import FideClientWithPagination
from python_fide.parsing.news_parsing import news_detail_parsing
from python_fide.config.news_config import (
    NewsDetailConfig,
    NewsLatestConfig
)
from python_fide.types.core import (
    FideNews,
    FideNewsDetail,
    FideNewsID
)

class FideNewsClient(FideClientWithPagination):
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
            fide_type=FideNews
        )

        return pagination.records

    def get_news_detail(
        self,
        fide_news: Union[FideNews, FideNewsID]
    ) -> Optional[FideNewsDetail]:
        """
        """
        config = NewsDetailConfig.from_news_object(
            fide_news=fide_news
        )

        # Request from API to get profile detail JSON response
        fide_url = config.endpointize(base_url=self.base_url)
        response = self._fide_request(fide_url=fide_url)

        # Validate and parse profile detail fields from response
        player_detail = news_detail_parsing(
            response=response
        )

        # If the ID from the found Fide news does not match the
        # Fide ID passed in as an argument, then return None
        if (
            player_detail is not None and
            player_detail.news.news_id != config.fide_news_id
        ):
            return
        return player_detail