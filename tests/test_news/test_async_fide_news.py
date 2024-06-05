from typing import Union
from unittest import mock

import pytest
from python_fide.clients_async import AsyncFideNewsClient
from python_fide import (
    FideNews,
    FideNewsDetail,
    FideNewsID
)

from tests.utils import MockedResponse
from tests.test_news.common_news import (
    FIDE_NEWS_DETAIL_CANDIDATES_ONE,
    FIDE_NEWS_DETAIL_CANDIDATES_TWO,
    FIDE_NEWS_PARAMETERS_CANDIDATES_ONE,
    FIDE_NEWS_PARAMETERS_CANDIDATES_TWO
)

fide_news_client = AsyncFideNewsClient()

@pytest.mark.asyncio
@pytest.mark.parametrize(
    'fide_news', FIDE_NEWS_PARAMETERS_CANDIDATES_ONE
)
@mock.patch(
    target='httpx.AsyncClient.get',
    side_effect=MockedResponse(filename='fide_news_candidates_one.json').mock_response,
    autospec=True
)
async def test_async_news_mock_detail_candidates_one(
    _, fide_news: Union[FideNews, FideNewsID]
) -> None:
    """Testing the news detail functionality for example one."""
    news_detail: FideNewsDetail = await fide_news_client.get_news_detail(
        fide_news=fide_news
    )
    assert news_detail == FIDE_NEWS_DETAIL_CANDIDATES_ONE


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'fide_news', FIDE_NEWS_PARAMETERS_CANDIDATES_TWO
)
@mock.patch(
    target='httpx.AsyncClient.get',
    side_effect=MockedResponse(filename='fide_news_candidates_two.json').mock_response,
    autospec=True
)
async def test_async_news_mock_detail_candidates_two(
    _, fide_news: Union[FideNews, FideNewsID]
) -> None:
    """Testing the news detail functionality for example two."""
    news_detail: FideNewsDetail = await fide_news_client.get_news_detail(
        fide_news=fide_news
    )
    assert news_detail == FIDE_NEWS_DETAIL_CANDIDATES_TWO