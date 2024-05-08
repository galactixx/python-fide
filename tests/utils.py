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
            raise RequestException("Incorrect status code...")


class MockedResponse:
    def __init__(self, filename: str):
        self._response = load_json_file(filename=filename)
    
    def mock_response(self, *args, **kwargs) -> MockResponse:
        return MockResponse(
            json_data=self._response, status_code=200
        )