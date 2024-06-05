from typing import Any, Dict, Union
from unittest import mock

import pytest
from python_fide.clients_sync import FideNewsClient
from python_fide import (
    FideNews,
    FideNewsDetail,
    FideNewsID,
    InvalidFideIDError
)

from python_fide.parsing.news_parsing import news_detail_parsing
from tests.utils import (
    load_json_file,
    MockedResponse
)
from tests.test_news.common_news import (
    FIDE_NEWS_DETAIL_CANDIDATES_ONE,
    FIDE_NEWS_DETAIL_CANDIDATES_TWO,
    FIDE_NEWS_PARAMETERS_CANDIDATES_ONE,
    FIDE_NEWS_PARAMETERS_CANDIDATES_TWO
)

fide_news_client = FideNewsClient()

def test_news_detail_parsing() -> None:
    """Testing the news detail parsing functions."""
    fide_response_one: Dict[str, Any] = load_json_file(filename='fide_news_candidates_one.json')
    news_detail: FideNewsDetail = news_detail_parsing(response=fide_response_one)
    assert news_detail == FIDE_NEWS_DETAIL_CANDIDATES_ONE

    fide_response_two: Dict[str, Any] = load_json_file(filename='fide_news_candidates_two.json')
    news_detail: FideNewsDetail = news_detail_parsing(response=fide_response_two)
    assert news_detail == FIDE_NEWS_DETAIL_CANDIDATES_TWO


@pytest.mark.parametrize(
    'fide_news', FIDE_NEWS_PARAMETERS_CANDIDATES_ONE
)
@mock.patch(
    target='requests.get',
    side_effect=MockedResponse(filename='fide_news_candidates_one.json').mock_response,
    autospec=True
)
def test_news_mock_detail_candidates_one(
    _, fide_news: Union[FideNews, FideNewsID]
) -> None:
    """Testing the news detail functionality for example one."""
    news_detail: FideNewsDetail = fide_news_client.get_news_detail(
        fide_news=fide_news
    )
    assert news_detail == FIDE_NEWS_DETAIL_CANDIDATES_ONE


@pytest.mark.parametrize(
    'fide_news', FIDE_NEWS_PARAMETERS_CANDIDATES_TWO
)
@mock.patch(
    target='requests.get',
    side_effect=MockedResponse(filename='fide_news_candidates_two.json').mock_response,
    autospec=True
)
def test_news_mock_detail_candidates_two(
    _, fide_news: Union[FideNews, FideNewsID]
) -> None:
    """Testing the news detail functionality for example two."""
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
    """Testing the InvalidFideIDError for the FideNewsID class."""
    with pytest.raises(InvalidFideIDError) as exc_info:
        _ = FideNewsID(entity_id=fide_news_id)
    assert str(exc_info.value) == error