from typing import Any, Dict
from unittest import mock
import pytest

import pytest
from python_fide import (
    Date,
    FideNews,
    FideNewsClient,
    FideNewsDetail,
    FideNewsID,
    InvalidFideIDError
)

from python_fide.parsing.news_parsing import news_detail_parsing
from tests.utils import (
    load_json_file,
    mock_request
)
from tests.examples.parameters.news_parameters import (
    FIDE_NEWS_DETAIL_2970,
    FIDE_NEWS_DETAIL_2981
)

fide_news_client = FideNewsClient()

def _mock_request_news_2970(*args, **kwargs):
    response = load_json_file(filename='fide_news_2970.json')
    return mock_request(response=response)


def _mock_request_news_2981(*args, **kwargs):
    response = load_json_file(filename='fide_news_2981.json')
    return mock_request(response=response)


def test_news_detail_parsing() -> None:
    """
    """
    fide_response_one: Dict[str, Any] = load_json_file(filename='fide_news_2970.json')
    event_detail: FideNewsDetail = news_detail_parsing(response=fide_response_one)
    assert event_detail == FIDE_NEWS_DETAIL_2970

    fide_response_two: Dict[str, Any] = load_json_file(filename='fide_news_2981.json')
    event_detail: FideNewsDetail = news_detail_parsing(response=fide_response_two)
    assert event_detail == FIDE_NEWS_DETAIL_2981


@mock.patch(
    'requests.get', side_effect=_mock_request_news_2970, autospec=True
)
def test_news_mock_detail_2970(_) -> None:
    """
    """
    news_detail: FideNewsDetail = fide_news_client.get_news_detail(
        fide_news=FideNewsID(entity_id='2970')
    )
    assert news_detail == FIDE_NEWS_DETAIL_2970

    news_detail: FideNewsDetail = fide_news_client.get_news_detail(
        fide_news=FideNewsID(entity_id=2970)
    )
    assert news_detail == FIDE_NEWS_DETAIL_2970

    news_detail: FideNewsDetail = fide_news_client.get_news_detail(
        fide_news=FideNews(
        name='FIDE Candidates: Race for first wide open as second half begins', news_id=2970,
        posted_at=Date(date_iso='2024-04-14', date_original='2024-04-14 05:37:05', date_original_format='%Y-%m-%d %H:%M:%S')
     )
    )
    assert news_detail == FIDE_NEWS_DETAIL_2970


@mock.patch(
    'requests.get', side_effect=_mock_request_news_2981, autospec=True
)
def test_news_mock_detail_2981(_) -> None:
    """
    """
    news_detail: FideNewsDetail = fide_news_client.get_news_detail(
        fide_news=FideNewsID(entity_id='2981')
    )
    assert news_detail == FIDE_NEWS_DETAIL_2981

    news_detail: FideNewsDetail = fide_news_client.get_news_detail(
        fide_news=FideNewsID(entity_id=2981)
    )
    assert news_detail == FIDE_NEWS_DETAIL_2981

    news_detail: FideNewsDetail = fide_news_client.get_news_detail(
        fide_news=FideNews(
        name="Four in the race for first in FIDE Candidates; Tan solely on top in Women’s event", news_id=2981,
        posted_at=Date(date_iso='2024-04-19', date_original='2024-04-19 05:23:57', date_original_format='%Y-%m-%d %H:%M:%S')
    )
    )
    assert news_detail == FIDE_NEWS_DETAIL_2981


def test_news_error_invalid_fide_id() -> None:
    """
    """
    with pytest.raises(InvalidFideIDError) as exc_info:
        _ = FideNewsID(entity_id='H19JF433')
    assert str(exc_info.value) == 'invalid Fide ID entered, must be an integer (as str in int type)'

    with pytest.raises(InvalidFideIDError) as exc_info:
        _ = FideNewsID(entity_id='0023FFH8')
    assert str(exc_info.value) == 'invalid Fide ID entered, must be an integer (as str in int type)'

    with pytest.raises(InvalidFideIDError) as exc_info:
        _ = FideNewsID(entity_id='003953322')
    assert str(exc_info.value) == 'invalid Fide ID entered, cannot start with a zero'