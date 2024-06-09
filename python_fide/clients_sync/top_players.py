from typing import List, Optional

from python_fide.enums import RatingCategory
from python_fide.clients_sync.base_client import FideClient
from python_fide.config.top_players_config import TopPlayersConfig
from python_fide.parsing.top_players_parsing import top_standard_players_parsing
from python_fide.types.core import FideTopPlayer

class FideTopPlayersClient(FideClient):
    """
    A Fide top players client to pull all player rankings data from the Fide
    API. Can pull top 10 and 100 rankings for any category (OPEN, WOMEN, JUNIORS,
    GIRLS) and country, among other parameters.
    """
    def __init__(self):
        self.base_url = 'https://app.fide.com/api/v1/client/players/'

    def get_top_ten_standard_rankings(
        self,
        limit: Optional[int] = None,
        categories: Optional[List[RatingCategory]] = None
    ) -> List[FideTopPlayer]:
        """
        Will return a list of FideTopPlayer objects each representing a player
        in the top ten standard rating rankings.

        limit (int | None): An integer of the maximum number of events to parse
            and return, cannot be more than 10. If no limit is specified then it
            defaults to 10.
        categories (List[RatingCategory] | None): A list of RatingCategory values
            each representing a chess category (OPEN, WOMEN, JUNIORS, GIRLS). If no
            category is specified, all categories will be included.

        Returns:
            List[FideTopPlayer]: A list of FideTopPlayer objects, each representing
                a player from the top ten standard rating rankings.
        """
        config = TopPlayersConfig(limit=limit, categories=categories)

        # Request from API to get players JSON response
        response = self._fide_request(fide_url=self.base_url)

        # Validate and parse player fields from response
        top_players = top_standard_players_parsing(
            limit=config.limit, response=response, categories=config.categories
        )

        return top_players