import os
from typing import Any, Dict
import json

from requests import RequestException

def _build_response_path(filename: str) -> str:
    """"""
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'examples', filename
    )


def load_json_file(filename: str) -> Dict[str, Any]:
    """"""
    response_path: str = _build_response_path(filename=filename)
    with open(response_path, encoding='utf-8') as json_file:
        fide_response = json.load(json_file)

    return fide_response


def mock_request(response: Dict[str, Any]):
    class MockResponse:
        def __init__(
            self,
            json_data: Dict[str, Any],
            status_code: int
        ):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code != 200:
                raise RequestException("Non-2xx status code detected")
            
    return MockResponse(
        json_data=response, status_code=200
    )