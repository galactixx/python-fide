from typing import Any, Dict

import requests
from requests import HTTPError
from faker import Faker

from python_fide.types import URLInfo
from python_fide.exceptions import NoResultsError

def fide_request(
    url_info: URLInfo,
    params: Dict[str, Any] = {}
) -> Dict[str, Any]:
    """
    """
    user_agent: str = Faker().user_agent()

    response = requests.get(
        url=url_info.url,
        params=params,
        headers={
            **url_info.headers,
            'User-Agent': user_agent
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