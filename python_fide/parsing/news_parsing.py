from typing import Any, Dict, List, Optional

from pydantic import ValidationError

from python_fide.types import (
    ClientNotFound,
    FideNews,
    FideNewsDetail
)

def news_latest_parsing(record: Dict[str, Any]) -> List[FideNews]:
    """
    """
    fide_news = FideNews.model_validate(record)
    return fide_news


def news_detail_parsing(response: Dict[str, dict]) -> Optional[FideNewsDetail]:
    """
    """
    # This is a search by Fide ID, thus there should never be a response
    # that has more than one item, although there can be a response with no items
    no_results = True
    try:
        _ = ClientNotFound.model_validate(response)
    except ValidationError:
        no_results = False

    if no_results:
        return
    else:
        fide_detail = FideNewsDetail.from_validated_model(
            news=response['data']
        )
        return fide_detail
