from typing import Any, Dict, Optional

import requests
from requests import HTTPError
from faker import Faker

from python_fide.types.adapters import HolisticAdapter
from python_fide.pagination import FidePagination
from python_fide.types.base import BaseRecordValidatorModel
from python_fide.config.base_config import BaseParameterConfig

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
        return response.json()
    
    def _fide_request_wrapped(
        self,
        fide_url: str,
        params: Dict[str, Any] = {}
    ) -> Optional[Dict[str, Any]]:
        """
        """
        try:
            response_json = self._fide_request(
                fide_url=fide_url, params=params
            )
        except HTTPError as e:
            if e.response.status_code == 500:
                return
            else:
                raise HTTPError(e)
        else:
            return response_json
        

class FideClientWithPagination(FideClient):
    """
    """
    def _paginatize(
        self,
        limit: int,
        base_url: str,
        config: BaseParameterConfig,
        fide_type: BaseRecordValidatorModel
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