from typing import Any, Dict

from pydantic import ValidationError

from python_fide.types.core import ClientNotFound

def detect_client_error(response: Dict[str, Any]) -> bool:
    """
    Detection of JSON error responses that occur when requesting from the
    event and news detail endpoints. If there are no results an error response
    will be returned.

    Args:
        response (Dict[str, Any]): A dictionary representation of the JSON response.

    Returns:
        bool: A boolean indicating whether the error response is present.
    """
    no_results = True
    try:
        _ = ClientNotFound.model_validate(response)
    except ValidationError:
        no_results = False
    return no_results