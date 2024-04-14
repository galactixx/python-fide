from typing import Any, Dict

def find_result_pages(response: Dict[str, Any]) -> int:
    """
    """
    return response['meta']['last_page']