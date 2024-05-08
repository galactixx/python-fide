from typing import Any, Dict, Union
from unittest import mock
import pytest

import pytest
from python_fide import (
    Date,
    FideNews,
    FideNewsCategory,
    FideNewsClient,
    FideNewsContent,
    FideNewsDetail,
    FideNewsID,
    FideNewsTopic,
    InvalidFideIDError
)

from python_fide.parsing.news_parsing import news_detail_parsing
from tests.utils import (
    load_json_file,
    MockedResponse
)

fide_news_client = FideNewsClient()

FIDE_NEWS_DETAIL_CANDIDATES_ONE = FideNewsDetail(
    topic=FideNewsTopic(topic_id=20, topic_name='Candidates'),
    category=FideNewsCategory(category_id=1, category_name='Chess news'),
    contents=[
        FideNewsContent(
            content="After the rest day, the second half of the FIDE Candidates kicked off on April 13...",
            images=list()
        )
    ],
    created_at=Date(
        date_iso='2024-04-14', date_original='2024-04-14 05:49:27', date_original_format='%Y-%m-%d %H:%M:%S'
    ),
    updated_at=Date(
        date_iso='2024-04-14', date_original='2024-04-14 05:49:27', date_original_format='%Y-%m-%d %H:%M:%S'
    ),
    news=FideNews(
        title='FIDE Candidates: Race for first wide open as second half begins',
        news_id=2970,
        posted_at=Date(
            date_iso='2024-04-14', date_original='2024-04-14 05:37:05', date_original_format='%Y-%m-%d %H:%M:%S'
        )
    )
)

FIDE_NEWS_DETAIL_CANDIDATES_TWO = FideNewsDetail(
    topic=FideNewsTopic(topic_id=20, topic_name='Candidates'),
    category=FideNewsCategory(category_id=1, category_name='Chess news'),
    contents=[
        FideNewsContent(
            content='The FIDE Candidates Tournament is getting more and more exciting with each and every passing day...',
            images=list()
        )
    ],
    created_at=Date(
        date_iso='2024-04-19', date_original='2024-04-19 05:41:42', date_original_format='%Y-%m-%d %H:%M:%S'
    ),
    updated_at=Date(
        date_iso='2024-04-19', date_original='2024-04-19 05:41:42', date_original_format='%Y-%m-%d %H:%M:%S'
    ),
    news=FideNews(
        title='Four in the race for first in FIDE Candidates; Tan solely on top in Women’s event',
        news_id=2981,
        posted_at=Date(
            date_iso='2024-04-19', date_original='2024-04-19 05:23:57', date_original_format='%Y-%m-%d %H:%M:%S'
        )
    )
)

def test_news_detail_parsing() -> None:
    """
    """
    fide_response_one: Dict[str, Any] = load_json_file(filename='fide_news_candidates_one.json')
    news_detail: FideNewsDetail = news_detail_parsing(response=fide_response_one)
    assert news_detail == FIDE_NEWS_DETAIL_CANDIDATES_ONE

    fide_response_two: Dict[str, Any] = load_json_file(filename='fide_news_candidates_two.json')
    news_detail: FideNewsDetail = news_detail_parsing(response=fide_response_two)
    assert news_detail == FIDE_NEWS_DETAIL_CANDIDATES_TWO


@pytest.mark.parametrize(
    'fide_news', [
        FideNewsID(entity_id='2970'),
        FideNewsID(entity_id=2970),
        FIDE_NEWS_DETAIL_CANDIDATES_ONE.news
    ]
)
@mock.patch(
    target='requests.get',
    side_effect=MockedResponse(filename='fide_news_candidates_one.json').mock_response,
    autospec=True
)
def test_news_mock_detail_candidates_one(_, fide_news: Union[FideNews, FideNewsID]) -> None:
    """
    """
    news_detail: FideNewsDetail = fide_news_client.get_news_detail(
        fide_news=fide_news
    )
    assert news_detail == FIDE_NEWS_DETAIL_CANDIDATES_ONE


@pytest.mark.parametrize(
    'fide_news', [
        FideNewsID(entity_id='2981'),
        FideNewsID(entity_id=2981),
        FIDE_NEWS_DETAIL_CANDIDATES_TWO.news
    ]
)
@mock.patch(
    target='requests.get',
    side_effect=MockedResponse(filename='fide_news_candidates_two.json').mock_response,
    autospec=True
)
def test_news_mock_detail_candidates_two(_, fide_news: Union[FideNews, FideNewsID]) -> None:
    """
    """
    news_detail: FideNewsDetail = fide_news_client.get_news_detail(
        fide_news=fide_news
    )
    assert news_detail == FIDE_NEWS_DETAIL_CANDIDATES_TWO


@pytest.mark.parametrize(
    'fide_news_id, error', [
        ('H19JF433', 'invalid Fide ID entered, must be an integer (as str in int type)'),
        ('0023FFH8', 'invalid Fide ID entered, must be an integer (as str in int type)'),
        ('003953322', 'invalid Fide ID entered, cannot start with a zero')
    ]
)
def test_news_error_invalid_fide_id(fide_news_id: str, error: str) -> None:
    """
    """
    with pytest.raises(InvalidFideIDError) as exc_info:
        _ = FideNewsID(entity_id=fide_news_id)
    assert str(exc_info.value) == error