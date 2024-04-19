from typing import List, Optional

from python_fide.enums import RatingCategory
from python_fide.clients.base_client import FideClient
from python_fide.config.top_players_config import TopPlayersConfig
from python_fide.parsing.top_players_parsing import top_standard_players_parsing
from python_fide.types.core import FideTopPlayer

class FideTopPlayersClient(FideClient):
    """
    """
    def __init__(self):
        self.base_url = (
            'https://app.fide.com/api/v1/client/players/'
        )

    def get_top_standard_players(
        self,
        limit: int = 10,
        categories: Optional[List[RatingCategory]] = None
    ) -> List[FideTopPlayer]:
        """
        """
        config = TopPlayersConfig(categories=categories)

        # Request from API to get players JSON response
        response = self._fide_request(
            fide_url=self.base_url
        )

        # Validate and parse player fields from response
        top_players = top_standard_players_parsing(
            limit=limit,
            response=response,
            categories=config.categories
        )

        return top_players