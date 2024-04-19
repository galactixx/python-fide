from typing import Any, Dict, Optional

from python_fide.parsing.common_parsing import detect_client_error
from python_fide.types_adapter import PartialDictAdapter
from python_fide.types import (
    FideNews,
    FideNewsDetail
)

def news_latest_parsing(record: Dict[str, Any]) -> FideNews:
    """
    """
    fide_news = FideNews.model_validate(record)
    return fide_news


def news_detail_parsing(response: Dict[str, dict]) -> Optional[FideNewsDetail]:
    """
    """
    # This is a search by Fide ID, thus there should never be a response
    # that has more than one item, although there can be a response with no items
    no_results = detect_client_error(response=response)

    if no_results:
        return
    else:
        partial_adapter = PartialDictAdapter.model_validate(response)
        fide_detail = FideNewsDetail.from_validated_model(
            news=partial_adapter.data
        )
        return fide_detail
