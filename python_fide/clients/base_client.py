from typing import Any, Callable, Dict, TypeVar

import requests
from requests import HTTPError
from faker import Faker

from python_fide.exceptions import NoResultsError
from python_fide.pagination import FidePagination
from python_fide.config.base_config import BaseParameterConfig
from python_fide.parsing.common_parsing import find_result_pages

T = TypeVar('T')

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
        
    def _paginatize(
        self,
        limit: int,
        base_url: str,
        config: BaseParameterConfig,
        parser: Callable[[Dict[str, Any]], T]
    ) -> FidePagination:
        """
        """
        fide_pagination = FidePagination(limit=limit)

        while fide_pagination.loop_continue:
            params = config.add_pagination_to_params(
                page=fide_pagination.current_page,
                parameters=config.parameterize
            )

            response_json = self._fide_request(
                fide_url=base_url, params=params
            )

            if fide_pagination.overflow_pages is None:
                fide_pagination.overflow_pages = find_result_pages(
                    response=response_json
                )

            # Parse and gather all news from response
            for record in response_json['data']:
                parsed_record = parser(record=record)

                fide_pagination.update_status(record=parsed_record)
                if not fide_pagination.loop_continue:
                    return fide_pagination

        return fide_pagination