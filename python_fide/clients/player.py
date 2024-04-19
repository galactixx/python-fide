from typing import List, Optional, Union

from python_fide.clients.base_client import FideClient
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

class FidePlayerClient(FideClient):
    """
    """
    def __init__(self):
        self.base_url = 'https://ratings.fide.com/'
        self.base_url_detail = (
            'https://app.fide.com/api/v1/client/players/'
        )

    def _consolidate_fide_player(
        self,
        fide_player: Union[FidePlayer, FidePlayerID]
    ) -> FidePlayer:
        """
        """
        if isinstance(fide_player, FidePlayerID):
            fide_player_detail = self.get_fide_player_detail(fide_player=fide_player)

            if fide_player_detail is None:
                raise InvalidFideIDError(
                    'Fide ID is invalid and has no link to a Fide rated player'
                )
            else:
                return fide_player_detail.player
        return fide_player

    def get_fide_player_detail(
        self,
        fide_player: Union[FidePlayer, FidePlayerID]
    ) -> Optional[FidePlayerDetail]:
        """
        """
        config = PlayerDetailConfig(fide_player_id=fide_player)

        # Request from API to get profile detail JSON response
        fide_url = config.endpointize(base_url=self.base_url_detail)
        response = self._fide_request(fide_url=fide_url)

        # Validate and parse profile detail fields from response
        player_detail = player_detail_parsing(
            response=response
        )

        # If the ID from the found Fide player does not match the
        # Fide ID passed in as an argument, then return None
        if (
            player_detail is not None and
            player_detail.player.player_id != config.fide_player_id
        ):
            return
        return player_detail

    def get_fide_player_opponents(
        self,
        fide_player: Union[FidePlayer, FidePlayerID]
    ) -> List[FidePlayerBasic]:
        """
        """
        config = PlayerOpponentsConfig(fide_player_id=fide_player)

        # Request from API to get player JSON response
        _ = self._consolidate_fide_player(
            fide_player=fide_player
        )

        # Request from API to get profile opponents JSON response
        fide_url = build_url(
            base=self.base_url, segments='a_data_opponents.php?'
        )
        response = self._fide_request(
            fide_url=fide_url, params=config.parameterize
        )

        # Validate and parse profile detail fields from response
        opponents = player_opponents_parsing(response=response)

        return opponents

    def get_fide_player_rating_progress_chart(
        self,
        fide_player: Union[FidePlayer, FidePlayerID],
        period: Optional[Period] = None
    ) -> List[FidePlayerRating]:
        """
        """
        config = PlayerChartsConfig(
            fide_player_id=fide_player, period=period
        )

        # Request from API to get player JSON response
        fide_player = self._consolidate_fide_player(
            fide_player=fide_player
        )

        # Request from API to get charts JSON response
        fide_url = build_url(
            base=self.base_url, segments='a_chart_data.phtml?'
        )
        response = self._fide_request(
            fide_url=fide_url, params=config.parameterize
        )

        # Validate and parse ratings chart fields from response
        rating_charts = player_charts_parsing(
            fide_player=fide_player,
            response=response
        )
        return rating_charts

    def get_fide_player_game_stats(
        self,
        fide_player: Union[FidePlayer, FidePlayerID],
        fide_player_opponent: Union[FidePlayer, FidePlayerID] = None
    ) -> List[FidePlayerGameStats]:
        """
        """
        config = PlayerStatsConfig(
            fide_player_id=fide_player,
            fide_player_opponent=fide_player_opponent
        )

        # Retrieve the player structure for both the player
        # and the opponent
        fide_player = self._consolidate_fide_player(
            fide_player=fide_player
        )
        fide_player_opponent = self._consolidate_fide_player(
            fide_player=fide_player_opponent
        )

        # Request from API to get game stats JSON response
        fide_url = build_url(
            base=self.base_url, segments='a_data_stats.php?'
        )
        response = self._fide_request(
            fide_url=fide_url, params=config.parameterize
        )

        # Validate and parse game statistics from response
        game_stats = player_stats_parsing(
            fide_player=fide_player,
            fide_player_opponent=fide_player_opponent,
            response=response
        )
        return game_stats