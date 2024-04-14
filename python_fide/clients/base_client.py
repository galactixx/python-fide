from typing import Any, Dict

import requests
from requests import HTTPError
from faker import Faker

from python_fide.exceptions import NoResultsError

class FideClient(object):
    """
    """
    user_agent: str = Faker().user_agent()
    
    def _fide_request(
        self,
        fide_url: str,
        params: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        """
        """
        try:
            response = requests.get(
                url=fide_url,
                params=params,
                headers={
                    "Accept": "*/*",
                    "Accept-Language": "en-US,en;q=0.9,bg;q=0.8",
                    "X-Requested-With": "XMLHttpRequest",
                    'User-Agent': self.user_agent
                }
            )
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