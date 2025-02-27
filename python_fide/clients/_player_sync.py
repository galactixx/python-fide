import json
from typing import List, Optional

from python_fide._enums import RatingPeriod
from python_fide._exceptions import InvalidFidePlayerError
from python_fide._parsing import (
    player_charts_parsing,
    player_opponents_parsing,
    player_stats_parsing,
)
from python_fide._typing import FidePlayerLike
from python_fide.clients._base import SyncFideClient
from python_fide.config._player import (
    PlayerChartsConfig,
    PlayerOpponentsConfig,
    PlayerStatsConfig,
)
from python_fide.types._core import FidePlayer, FidePlayerGameStats, FidePlayerRating
from python_fide.utils._general import build_url


class FidePlayerClient(SyncFideClient):
    """
    A synchronous Fide player client to pull all player specific data
    from the Fide API. Provides methods to pull a players opponents,
    historical month ratings, and complete game stats.
    """

    def __init__(self) -> None:
        self.base_url = "https://ratings.fide.com/"

    def get_opponents(self, player: FidePlayerLike) -> List[FidePlayer]:
        """
        Given a `FidePlayer` or `FidePlayerID` instance, will return a list
        of `FidePlayer` instances each representing an opponent (another
        Fide player) that the player has faced during their chess career.

        The data retrieved through this endpoint not only provides a
        comprehensive account of the history of a specific Fide player, but
        can be used to filter the data returned from the game stats endpoint.

        Args:
            player (`FidePlayer` | `FidePlayerID`): A `FidePlayer` or
                `FidePlayerID` instance.

        Returns:
            List[`FidePlayer`]: A list of `FidePlayer` instances each
                representing an opponent the player in question has faced.
        """
        config = PlayerOpponentsConfig(fide_id=player)

        # Request from API to get profile opponents JSON response
        fide_url = build_url(base=self.base_url, segments="a_data_opponents.php?")
        try:
            response = self._fide_request(fide_url=fide_url, params=config.parameterize)
        except json.JSONDecodeError:
            raise InvalidFidePlayerError(
                "Fide ID does not link to an existing Fide player."
            )

        # Validate and parse profile detail fields from response
        opponents = player_opponents_parsing(response=response)
        return opponents

    def get_rating_progress_chart(
        self, player: FidePlayerLike, period: Optional[RatingPeriod] = None
    ) -> List[FidePlayerRating]:
        """
        Given a `FidePlayer` or `FidePlayerID` instance, will return a list of
        `FidePlayerRating` instances each representing a set of ratings
        (standard, rapid, and blitz) for a specific month. Also included
        with each format is the number of games played in that month.

        A period can also be included, which will filter the ratings based
        on period of time (in years). Using the RatingPeriod data type, options
        available are ONE_YEAR, TWO_YEARS, THREE_YEARS, FIVE_YEARS, and
        ALL_YEARS. If no period is specified, then it defaults to ALL_YEARS.

        Args:
            player (`FidePlayer` | `FidePlayerID`): A `FidePlayer` or
                `FidePlayerID` instance.
            period (`RatingPeriod` | None): An enum which allows filtering of
                the ratings data by period of time.

        Returns:
            List[`FidePlayerRating`]: A list of `FidePlayerRating` instances,
                each representing a set of ratings for a specific month.
        """
        config = PlayerChartsConfig(fide_id=player, period=period)

        # Request from API to get charts JSON response
        fide_url = build_url(base=self.base_url, segments="a_chart_data.phtml?")
        response = self._fide_request(fide_url=fide_url, params=config.parameterize)

        # Validate and parse ratings chart fields from response
        rating_charts = player_charts_parsing(player=player, response=response)
        return rating_charts

    def get_game_stats(
        self, player: FidePlayerLike, opponent: Optional[FidePlayerLike] = None
    ) -> FidePlayerGameStats:
        """
        Given a `FidePlayer` or `FidePlayerID` instance, will return a
        `FidePlayerGameStats` instance representing the entire game history for
        a specific player. This includes the number of games won, drawn, and
        lost when playing for white and black pieces.

        Another `FidePlayer` or `FidePlayerID` object can be passed for the
        'fide_player_opponent' parameter, which will filter the data to
        represent the game stats when facing this opponent. If no argument is
        passed then it will return the entire game history.

        Args:
            player (`FidePlayer` | `FidePlayerID`): A FidePlayer or
                `FidePlayerID` instance.
            opponent (`FidePlayer` | `FidePlayerID` | None): A
                `FidePlayer` or `FidePlayerID` instance. Can also be None if
                the entire game history should be returned.

        Returns:
            `FidePlayerGameStats`: A `FidePlayerGameStats` instance consisting
                of game statistics for the given Fide player.
        """
        config = PlayerStatsConfig(fide_id=player, fide_id_opponent=opponent)

        # Request from API to get game stats JSON response
        fide_url = build_url(base=self.base_url, segments="a_data_stats.php?")
        response = self._fide_request(fide_url=fide_url, params=config.parameterize)

        # Validate and parse game statistics from response
        game_stats = player_stats_parsing(
            player=player, opponent=opponent, response=response
        )
        return game_stats
