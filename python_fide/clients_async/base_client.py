from typing import Any, Dict

import httpx
from faker import Faker


class AsyncFideClient(object):
    """
    Base client for interaction with the Fide API.
    """

    user_agent: str = Faker().user_agent()

    async def _fide_request(
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
        async with httpx.AsyncClient() as client:
            response = await client.get(
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
