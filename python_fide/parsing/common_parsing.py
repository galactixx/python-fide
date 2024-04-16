from typing import Any, Dict

from pydantic import ValidationError

from python_fide.types import ClientNotFound

def detect_client_error(response: Dict[str, Any]) -> bool:
    """
    """
    no_results = True
    try:
        _ = ClientNotFound.model_validate(response)
    except ValidationError:
        no_results = False
    return no_results