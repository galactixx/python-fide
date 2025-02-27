from typing import Any, Dict

import httpx
import requests
from faker import Faker


class BaseFideClient(object):
    """
    Base client for interaction with the Fide API.
    """

    user_agent: str = Faker().user_agent()


class AsyncFideClient(BaseFideClient):
    """
    Base client for interaction with the Fide API.
    """

    async def _fide_request(
        self, fide_url: str, params: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        """
        Private method which makes a generic request to a Fide API endpoint.
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


class SyncFideClient(BaseFideClient):
    """
    Base client for interaction with the Fide API.
    """

    def _fide_request(
        self, fide_url: str, params: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        """
        Private method which makes a generic request to a Fide API endpoint.
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
