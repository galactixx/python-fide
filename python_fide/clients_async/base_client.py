from typing import Any, Dict, Optional

import httpx
from httpx import HTTPStatusError
from faker import Faker

from python_fide.types.adapters import HolisticAdapter
from python_fide.pagination import FidePagination
from python_fide.types.base import BaseRecordPaginationModel
from python_fide.config.base_config import BaseParameterConfig

class AsyncFideClient(object):
    """
    Base client for interaction with the Fide API.
    """
    user_agent: str = Faker().user_agent()
    
    async def _fide_request(
        self,
        fide_url: str,
        params: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        """
        Private method which makes a generic request to a
        Fide API endpoint.

        Args:
            fide_url (str): A string URL representing a Fide
                API endpoint.
            params (Dict[str, Any]): The paramaters to include
                in the request.

        Returns:
            Dict[str, Any]: A dictionary representation of the
                JSON response.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
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
            return response.json()
    
    async def _fide_request_wrapped(
        self,
        fide_url: str,
        params: Dict[str, Any] = {}
    ) -> Optional[Dict[str, Any]]:
        """
        Private method which makes a specific request to the
        Fide player search endpoint. A separate method exists
        due to the API crashing if there are no results from
        a player search request.

        Args:
            fide_url (str): A string URL representing a Fide
                API endpoint.
            params (Dict[str, Any]): The paramaters to include
                in the request.

        Returns:
            Dict[str, Any] | None: A dictionary representation
                of the JSON response. Can return None if there
                was a 500 status code due to no results. 
        """
        try:
            async with httpx.AsyncClient() as client:
                response_json = await self._fide_request(
                    fide_url=fide_url, params=params
                )
        except HTTPStatusError as e:
            if e.response.status_code == 500:
                return
            else:
                raise HTTPStatusError(e)
        else:
            return response_json
        

class AsyncFideClientPaginate(AsyncFideClient):
    """
    Derived class of FideClient which adds pagination functionality.
    """
    async def _paginatize(
        self,
        limit: int,
        fide_url: str,
        config: BaseParameterConfig,
        fide_type: BaseRecordPaginationModel
    ) -> FidePagination:
        """
        A private method to run pagination for the Fide
        news and events API endpoints.

        Args:
            limit (int): The maximum number of records to
                pull from endpoint.
            fide_url (str): A string URL representing a
                Fide API endpoint.
            config (BaseParameterConfig): A BaseParameterConfig
                instance used to create the params to include
                in the request.
            fide_type (BaseRecordPaginationModel): A
                BaseRecordPaginationModel instance defining the
                pydantic model used to validate and structure
                the API response.

        Returns:
            FidePagination: A FidePagination instance containing
                all records pulled from pagination.
        """
        fide_pagination = FidePagination(limit=limit)

        while fide_pagination.loop_continue:
            params = config.add_pagination_to_params(
                page=fide_pagination.current_page,
                parameters=config.parameterize
            )
            response_json = await self._fide_request(fide_url=fide_url, params=params)

            # Validate response using the HolisticAdapter model
            holistic = HolisticAdapter.model_validate(response_json)

            # Set number of pages to paginate if not already done
            if fide_pagination.overflow_pages is None:
                fide_pagination.overflow_pages = holistic.meta.page_last

            # Iterate through each record in main data, extracted
            # from response, and parse/validate each record
            for record in holistic.data:
                parsed_record = fide_type.from_validated_model(record=record)

                fide_pagination.update_status(record=parsed_record)
                if not fide_pagination.loop_continue:
                    return fide_pagination

        return fide_pagination