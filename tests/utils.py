import json
import os
from typing import Any, Dict

from requests import RequestException


def _build_response_path(filename: str) -> str:
    """Utility function to build path to example file for tests."""
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "examples", filename
    )


def load_json_file(filename: str) -> Dict[str, Any]:
    """Utility function to load example file as a JSON for tests."""
    response_path: str = _build_response_path(filename=filename)
    with open(response_path, encoding="utf-8") as json_file:
        fide_response = json.load(json_file)

    return fide_response


class MockResponse:
    """Mock response for patching."""

    def __init__(self, json_data: Dict[str, Any], status_code: int) -> None:
        self.json_data = json_data
        self.status_code = status_code

    def json(self) -> Dict[str, Any]:
        return self.json_data

    def raise_for_status(self) -> None:
        if self.status_code != 200:
            raise RequestException("Incorrect status code...")


class MockedResponse:
    """Class used to create a MockResponse object."""

    def __init__(self, filename: str) -> None:
        self._response = load_json_file(filename=filename)

    def mock_response(self, *args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse(json_data=self._response, status_code=200)
