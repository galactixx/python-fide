import requests
from requests import HTTPError
from faker import Faker

from python_fide.exceptions import NoResultsError
from python_fide.constants import (
    FIDE_HEADERS,
    FIDE_SEARCH_URL
)

class BaseClient(object):
    """
    """
    def __init__(self, fide_url: str):
        self._base_fide_url = fide_url
        self._user_agent = Faker().user_agent()

    def _fide_request(self, params: dict) -> dict:
        response = requests.get(
            url=self._base_fide_url,
            params=params,
            headers={
                **FIDE_HEADERS,
                'User-Agent': self._user_agent
            }
        )
        try:
            response.raise_for_status()
        except HTTPError as e:
            if str(e).startswith('500 Server Error'):
                raise NoResultsError()
            else:
                raise HTTPError(e)
        else:
            response_json = response.json()
            return response_json