import requests
from requests import HTTPError
from faker import Faker

from python_fide.types import URLInfo
from python_fide.exceptions import NoResultsError

class FideClient:
    """
    """
    def __init__(self):
        self._user_agent = Faker().user_agent()

    def __enter__(self):
        return self

    def __exit__(self):
        return False

    def request(
        self,
        params: dict,
        url_info: URLInfo
    ) -> dict:
        response = requests.get(
            url=url_info.url,
            params=params,
            headers={
                **url_info.headers,
                'User-Agent': self._user_agent
            }
        )
        try:
            response.raise_for_status()
        except HTTPError as e:
            # For some reason when requesting with some of the search methods
            # if there are no results the server returns a 500 error
            # Thus, we replace with our own customized error
            if e.response.status_code == 500:
                raise NoResultsError()
            else:
                raise HTTPError(e)
        else:
            response_json = response.json()
            return response_json