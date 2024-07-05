from typing import List, Optional, Union

from python_fide.clients_async.base_client import AsyncFideClient
from python_fide.enums import Period
from python_fide.exceptions import InvalidFideIDError
from python_fide.utils.general import build_url
from python_fide.types.core import (
    FidePlayer,
    FidePlayerBasic,
    FidePlayerDetail,
    FidePlayerGameStats,
    FidePlayerID,
    FidePlayerRating
)
from python_fide.parsing.player_parsing import (
    player_charts_parsing,
    player_detail_parsing,
    player_opponents_parsing,
    player_stats_parsing,
)
from python_fide.config.player_config import (
    PlayerChartsConfig,
    PlayerDetailConfig,
    PlayerOpponentsConfig,
    PlayerStatsConfig
)

class AsyncFidePlayerClient(AsyncFideClient):
    """
    A Fide player client to pull all player specific data from the Fide
    API. Provides methods to pull a players' detail, opponents, historical
    month ratings, and complete game stats. 
    """
    def __init__(self):
        self.base_url = 'https://ratings.fide.com/'
        self.base_url_detail = 'https://app.fide.com/api/v1/client/players/'

    async def _consolidate_fide_player(
        self,
        fide_player: Union[FidePlayer, FidePlayerID]
    ) -> FidePlayer:
        """
        A private method to ensure a Fide player ID passed in is valid. If a
        FidePlayer object is passed, then this is immediately returned. Otherwise
        if a FidePlayerID object is passed, then the Fide ID is validated, player
        data is retrieved, and a FidePlayer object is returned.

        Args:
            fide_player (FidePlayer | FidePlayerID): A FidePlayer or FidePlayerID object.

        Returns:
            FidePlayer: A FidePlayer object.
        """
        if isinstance(fide_player, FidePlayerID):
            fide_player_detail = await self.get_fide_player_detail(
                fide_player=fide_player
            )

            if fide_player_detail is None:
                raise InvalidFideIDError(
                    'Fide ID is invalid and has no link to a Fide rated player'
                )
            else:
                return fide_player_detail.player
        return fide_player

    async def get_fide_player_detail(
        self,
        fide_player: Union[FidePlayer, FidePlayerID]
    ) -> Optional[FidePlayerDetail]:
        """
        Given a FidePlayer or FidePlayerID object, will return a FidePlayerDetail
        object containing further detail for a player. If the ID included does not
        link to a valid Fide player ID, then None is returned.
        
        Args:
            fide_player (FidePlayer | FidePlayerID): A FidePlayer or FidePlayerID object.

        Returns:
            FidePlayerDetail | None: A FidePlayerDetail object or if the Fide player
                ID is invalid, None.
        """
        config = PlayerDetailConfig(fide_player_id=fide_player)

        # Request from API to get profile detail JSON response
        fide_url = config.endpointize(base_url=self.base_url_detail)
        response = await self._fide_request(fide_url=fide_url)

        # Validate and parse profile detail fields from response
        player_detail = player_detail_parsing(response=response)

        # If the ID from the found Fide player does not match the
        # Fide ID passed in as an argument, then return None
        if (
            player_detail is not None and
            player_detail.player.player_id != config.fide_player_id
        ):
            return
        return player_detail

    async def get_fide_player_opponents(
        self,
        fide_player: Union[FidePlayer, FidePlayerID]
    ) -> List[FidePlayerBasic]:
        """
        Given a FidePlayer or FidePlayerID object, will return a list of FidePlayerBasic
        objects each representing an opponent (another Fide player) that the player has
        faced during their chess career.
         
        The data retrieved through this endpoint not only provides a comprehensive account
        of the history of a specific Fide player, but can be used to filter the data returned
        from the game stats endpoint.

        Args:
            fide_player (FidePlayer | FidePlayerID): A FidePlayer or FidePlayerID object.

        Returns:
            List[FidePlayerBasic]: A list of FidePlayerBasic objects each representing an
                opponent the player in question has faced.
        """
        config = PlayerOpponentsConfig(fide_player_id=fide_player)

        # Request from API to get player JSON response
        _ = await self._consolidate_fide_player(fide_player=fide_player)

        # Request from API to get profile opponents JSON response
        fide_url = build_url(
            base=self.base_url, segments='a_data_opponents.php?'
        )
        response = await self._fide_request(
            fide_url=fide_url, params=config.parameterize
        )

        # Validate and parse profile detail fields from response
        opponents = player_opponents_parsing(response=response)

        return opponents

    async def get_fide_player_rating_progress_chart(
        self,
        fide_player: Union[FidePlayer, FidePlayerID],
        period: Optional[Period] = None
    ) -> List[FidePlayerRating]:
        """
        Given a FidePlayer or FidePlayerID object, will return a list of FidePlayerRating
        objects each representing a set of ratings (standard, rapid, and blitz) for a specific
        month. Also included with each format is the number of games played in that month.

        A period can also be included, which will filter the ratings based on period of time
        (in years). Using the Period data type, options available are ONE_YEAR, TWO_YEARS,
        THREE_YEARS, FIVE_YEARS, and ALL_YEARS. If no period is specified, then it defaults to
        ALL_YEARS.
        
        Args:
            fide_player (FidePlayer | FidePlayerID): A FidePlayer or FidePlayerID object.
            period (Period | None): An enum which allows filtering of the ratings data by period
                of time.

        Returns:
            List[FidePlayerRating]: A list of FidePlayerRating objects, each reprsenting a set of
                ratings for a specific month.
        """
        config = PlayerChartsConfig(
            fide_player_id=fide_player, period=period
        )

        # Request from API to get player JSON response
        fide_player = await self._consolidate_fide_player(fide_player=fide_player)

        # Request from API to get charts JSON response
        fide_url = build_url(
            base=self.base_url, segments='a_chart_data.phtml?'
        )
        response = await self._fide_request(
            fide_url=fide_url, params=config.parameterize
        )

        # Validate and parse ratings chart fields from response
        rating_charts = player_charts_parsing(
            fide_player=fide_player, response=response
        )
        return rating_charts

    async def get_fide_player_game_stats(
        self,
        fide_player: Union[FidePlayer, FidePlayerID],
        fide_player_opponent: Optional[Union[FidePlayer, FidePlayerID]] = None
    ) -> FidePlayerGameStats:
        """
        Given a FidePlayer or FidePlayerID object, will return a FidePlayerGameStats
        object representing the entire game history for a specific player. This includes
        the number of games won, drawn, and lost when playing for white and black pieces.

        Another FidePlayer or FidePlayerID object can be passed for the 'fide_player_opponent'
        parameter, which will filter the data to represent the game stats when facing this
        opponent. If no argument is passed then it will return the entire game history.

        Args:
            fide_player (FidePlayer | FidePlayerID): A FidePlayer or FidePlayerID object.
            fide_player_opponent (FidePlayer | FidePlayerID | None): A FidePlayer or FidePlayerID
                object. Can also be None if the entire game history should be returned.

        Returns:
            FidePlayerGameStats: A FidePlayerGameStats object consisting of game statistics
                for the given Fide player.
        """
        config = PlayerStatsConfig(
            fide_player_id=fide_player,
            fide_player_opponent_id=fide_player_opponent
        )

        # Retrieve the player structure for both the player and the opponent
        fide_player = await self._consolidate_fide_player(fide_player=fide_player)
        fide_player_opponent = await self._consolidate_fide_player(
            fide_player=fide_player_opponent
        )

        # Request from API to get game stats JSON response
        fide_url = build_url(
            base=self.base_url, segments='a_data_stats.php?'
        )
        response = await self._fide_request(
            fide_url=fide_url, params=config.parameterize
        )

        # Validate and parse game statistics from response
        game_stats = player_stats_parsing(
            fide_player=fide_player,
            fide_player_opponent=fide_player_opponent,
            response=response
        )
        return game_stats