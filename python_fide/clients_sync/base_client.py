from typing import Any, Dict, Optional

import requests
from faker import Faker
from requests import HTTPError


class FideClient(object):
    """
    Base client for interaction with the Fide API.
    """

    user_agent: str = Faker().user_agent()

    def _fide_request(
        self, fide_url: str, params: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        """
        Private method which makes a generic request to a Fide API endpoint.

        Args:
            fide_url (str): A string URL representing a Fide API endpoint.
            params (Dict[str, Any]): The paramaters to include in the request.

        Returns:
            Dict[str, Any]: A dictionary representation of the JSON response.
        """
        response = requests.get(
            url=fide_url,
            params=params,
            headers={
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9,bg;q=0.8",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": self.user_agent,
            },
        )
        response.raise_for_status()
        return response.json()

    def _fide_request_wrapped(
        self, fide_url: str, params: Dict[str, Any] = {}
    ) -> Optional[Dict[str, Any]]:
        """
        Private method which makes a specific request to the Fide player
        search endpoint. A separate method exists due to the API crashing
        if there are no results from a player search request.

        Args:
            fide_url (str): A string URL representing a Fide API endpoint.
            params (Dict[str, Any]): The paramaters to include in the request.

        Returns:
            Dict[str, Any] | None: A dictionary representation of the JSON
                response. Can return None if there was a 500 status code due
                to no results.
        """
        try:
            response_json = self._fide_request(fide_url=fide_url, params=params)
        except HTTPError as e:
            if e.response.status_code == 500:
                return
            else:
                raise HTTPError(e)
        else:
            return response_json
