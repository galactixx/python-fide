from typing import Any, List, Dict, Optional

from pydantic import ValidationError

from python_fide.types import (
    ClientNotFound,
    FideEventDetail
)

def event_latest_parsing(record: Dict[str, Any]) -> List[FideEventDetail]:
    """
    """
    fide_event = FideEventDetail.from_validated_model(record)
    return fide_event


def event_detail_parsing(response: Dict[str, dict]) -> Optional[FideEventDetail]:
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
        fide_detail = FideEventDetail.from_validated_model(
            event=response['data']
        )
        return fide_detail