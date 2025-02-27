from typing import List, Optional

from python_fide.clients_async.base_client import AsyncFideClient
from python_fide.config.player_config import (
    PlayerChartsConfig,
    PlayerOpponentsConfig,
    PlayerStatsConfig,
)
from python_fide.enums import Period
from python_fide.parsing import (
    player_charts_parsing,
    player_opponents_parsing,
    player_stats_parsing,
)
from python_fide.types.core import (
    FidePlayer,
    FidePlayerGameStats,
    FidePlayerID,
    FidePlayerRating,
)
from python_fide.utils.general import build_url


class AsyncFidePlayerClient(AsyncFideClient):
    """
    A Fide player client to pull all player specific data from the Fide
    API. Provides methods to pull a players' detail, opponents, historical
    month ratings, and complete game stats.
    """

    def __init__(self):
        self.base_url = "https://ratings.fide.com/"

    async def get_opponents(
        self, fide_player: FidePlayerID
    ) -> List[FidePlayer]:
        """
        Given a FidePlayer or FidePlayerID object, will return a list
        of FidePlayer objects each representing an opponent (another
        Fide player) that the player has faced during their chess career.

        The data retrieved through this endpoint not only provides a
        comprehensive account of the history of a specific Fide player, but
        can be used to filter the data returned from the game stats endpoint.

        Args:
            fide_player (FidePlayer | FidePlayerID): A FidePlayer or
                FidePlayerID object.

        Returns:
            List[FidePlayer]: A list of FidePlayer objects each
                representing an opponent the player in question has faced.
        """
        config = PlayerOpponentsConfig(fide_player_id=fide_player)

        # Request from API to get profile opponents JSON response
        fide_url = build_url(base=self.base_url, segments="a_data_opponents.php?")
        response = await self._fide_request(
            fide_url=fide_url, params=config.parameterize
        )

        # Validate and parse profile detail fields from response
        opponents = player_opponents_parsing(response=response)

        return opponents

    async def get_rating_progress_chart(
        self,
        fide_id: FidePlayerID,
        period: Optional[Period] = None,
    ) -> List[FidePlayerRating]:
        """
        Given a FidePlayer or FidePlayerID object, will return a list of
        FidePlayerRating objects each representing a set of ratings
        (standard, rapid, and blitz) for a specific month. Also included
        with each format is the number of games played in that month.

        A period can also be included, which will filter the ratings based
        on period of time (in years). Using the Period data type, options
        available are ONE_YEAR, TWO_YEARS, THREE_YEARS, FIVE_YEARS, and
        ALL_YEARS. If no period is specified, then it defaults to ALL_YEARS.

        Args:
            fide_player (FidePlayer | FidePlayerID): A FidePlayer or
                FidePlayerID object.
            period (Period | None): An enum which allows filtering of the
                ratings data by period of time.

        Returns:
            List[FidePlayerRating]: A list of FidePlayerRating objects, each
                reprsenting a set of ratings for a specific month.
        """
        config = PlayerChartsConfig(fide_player_id=fide_id, period=period)

        # Request from API to get charts JSON response
        fide_url = build_url(base=self.base_url, segments="a_chart_data.phtml?")
        response = await self._fide_request(
            fide_url=fide_url, params=config.parameterize
        )

        # Validate and parse ratings chart fields from response
        rating_charts = player_charts_parsing(fide_id=fide_id, response=response)
        return rating_charts

    async def get_game_stats(
        self,
        fide_id: FidePlayerID,
        fide_id_opponent: Optional[FidePlayerID] = None,
    ) -> FidePlayerGameStats:
        """
        Given a FidePlayer or FidePlayerID object, will return a
        FidePlayerGameStats object representing the entire game history for
        a specific player. This includes the number of games won, drawn, and
        lost when playing for white and black pieces.

        Another FidePlayer or FidePlayerID object can be passed for the
        'fide_player_opponent' parameter, which will filter the data to
        represent the game stats when facing this opponent. If no argument is
        passed then it will return the entire game history.

        Args:
            fide_player (FidePlayer | FidePlayerID): A FidePlayer or
                FidePlayerID object.
            fide_player_opponent (FidePlayer | FidePlayerID | None): A
                FidePlayer or FidePlayerID object. Can also be None if the
                entire game history should be returned.

        Returns:
            FidePlayerGameStats: A FidePlayerGameStats object consisting of
                game statistics for the given Fide player.
        """
        config = PlayerStatsConfig(
            fide_player_id=fide_id, fide_player_opponent_id=fide_id_opponent
        )

        # Request from API to get game stats JSON response
        fide_url = build_url(base=self.base_url, segments="a_data_stats.php?")
        response = await self._fide_request(
            fide_url=fide_url, params=config.parameterize
        )

        # Validate and parse game statistics from response
        game_stats = player_stats_parsing(
            fide_id=fide_id,
            fide_id_opponent=fide_id_opponent,
            response=response,
        )
        return game_stats
