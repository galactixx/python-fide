from typing import Dict, Optional

from python_fide.types import FideEventDetail

def event_detail_parsing(response: Dict[str, dict]) -> Optional[FideEventDetail]:
    """
    """
    # This is a search by Fide ID, thus there should never be a response
    # that has more than one item, although there can be a response with no items
    if not response:
        return
    else:
        fide_detail = FideEventDetail.from_validated_model(
            event=response['data']
        )
        return fide_detail
    
# {"message":"Not Found","status":404}