from typing import List

from python_fide.constants.rating_cat import RatingCategory
from python_fide.clients.fide_client import fide_request
from python_fide.config.players_config import TopPlayersConfig
from python_fide.parsing.players_parsing import top_standard_players_parsing
from python_fide.constants.common import (
    FIDE_PLAYERS_URL,
    FIDE_RATINGS_HEADERS
)
from python_fide.types import (
    FideTopPlayer,
    URLInfo
)

FIDE_PLAYERS_INFO = URLInfo(
    url=FIDE_PLAYERS_URL, headers=FIDE_RATINGS_HEADERS
)

def get_top_standard_players(
    categories: List[RatingCategory],
    limit: int = 10
) -> List[FideTopPlayer]:
    """
    """
    config = TopPlayersConfig(categories=categories)

    # Request from API to get players JSON response
    response = fide_request(url_info=FIDE_PLAYERS_INFO)

    # Validate and parse player fields from response
    top_players = top_standard_players_parsing(
        limit=limit,
        response=response,
        categories=config.categories
    )

    return top_players