from typing import List, Optional, Union

from python_fide.clients.fide_client import FideClient
from python_fide.constants.periods import Period
from python_fide.exceptions import InvalidFideIDError
from python_fide.clients.search import get_fide_player
from python_fide.types import (
    FidePlayer,
    FidePlayerGameStats,
    FidePlayerID,
    FidePlayerRating,
    URLInfo
)
from python_fide.parsing.profile_parsing import (
    profile_charts_parsing,
    profile_stats_parsing
)
from python_fide.constants.common import (
    FIDE_PROFILE_CHARTS_URL,
    FIDE_PROFILE_STATS_URL,
    FIDE_RATINGS_HEADERS
)
from python_fide.endpoint.profile_endpoint import (
    ProfileChartsConfig,
    ProfileStatsConfig
)

FIDE_CHARTS_INFO = URLInfo(
    url=FIDE_PROFILE_CHARTS_URL, headers=FIDE_RATINGS_HEADERS
)

FIDE_STATS_INFO = URLInfo(
    url=FIDE_PROFILE_STATS_URL, headers=FIDE_RATINGS_HEADERS
)

def get_profile_rating_progress_chart(
    fide_player: Union[FidePlayer, FidePlayerID],
    period: Optional[Period] = None
) -> List[FidePlayerRating]:
    """
    """
    with FideClient() as session:
        config = ProfileChartsConfig(
            fide_player=fide_player, period=period
        )

        # Request from API to get charts JSON response
        response = session.request(
            params=config.parameterize,
            url_info=FIDE_CHARTS_INFO
        )

        # Request from API to get player JSON response
        if isinstance(fide_player, FidePlayerID):
            fide_player = get_fide_player(query=fide_player)

            if fide_player is None:
                raise InvalidFideIDError()

        # Parse through all ratings returned from chart endpoint
        rating_charts = profile_charts_parsing(
            fide_player=fide_player,
            response=response
        )
        return rating_charts


def get_profile_game_stats(
    fide_player: Union[FidePlayer, FidePlayerID],
    fide_player_opponent: Union[FidePlayer, FidePlayerID] = None
) -> List[FidePlayerGameStats]:
    """
    """
    with FideClient() as session:
        config = ProfileStatsConfig(
            fide_player=fide_player,
            fide_player_opponent=fide_player_opponent
        )

        # Request from API to get game stats JSON response
        response = session.request(
            params=config.parameterize,
            url_info=FIDE_STATS_INFO,
        )

        game_stats = profile_stats_parsing(
            response=response
        )
        return game_stats