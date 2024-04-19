from typing import Any, Dict, Optional

from python_fide.parsing.common_parsing import detect_client_error
from python_fide.types import FideEventDetail
from python_fide.types_adapter import PartialDictAdapter

def event_latest_parsing(record: Dict[str, Any]) -> FideEventDetail:
    """
    """
    fide_event = FideEventDetail.from_validated_model(record)
    return fide_event


def event_detail_parsing(response: Dict[str, dict]) -> Optional[FideEventDetail]:
    """
    """
    # This is a search by Fide ID, thus there should never be a response
    # that has more than one item, although there can be a response with no items
    no_results = detect_client_error(response=response)

    if no_results:
        return
    else:
        partial_adapter = PartialDictAdapter.model_validate(response)
        fide_detail = FideEventDetail.from_validated_model(
            event=partial_adapter.data
        )
        return fide_detail