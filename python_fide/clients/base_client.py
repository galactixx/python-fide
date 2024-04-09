from typing import Dict

import requests
from requests import HTTPError
from faker import Faker

from python_fide.exceptions import NoResultsError

class BaseClient(object):
    """
    """
    def __init__(self):
        self._user_agent = Faker().user_agent()

    def _fide_request(
        self,
        fide_url: str,
        params: dict, 
        headers: Dict[str, str]
    ) -> dict:
        response = requests.get(
            url=fide_url,
            params=params,
            headers={
                **headers,
                'User-Agent': self._user_agent
            }
        )
        try:
            response.raise_for_status()
        except HTTPError as e:
            # For some reason when requesting with some of the search methods
            # if there are no results the server returns a 500 error
            if e.response.status_code == 500:
                raise NoResultsError()
            else:
                raise HTTPError(e)
        else:
            response_json = response.json()
            return response_json