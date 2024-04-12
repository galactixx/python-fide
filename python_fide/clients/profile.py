from typing import List, Optional, Union

from python_fide.clients.fide_client import fide_request
from python_fide.constants.periods import Period
from python_fide.exceptions import InvalidFideIDError
from python_fide.clients.search import get_fide_player
from python_fide.types import (
    FidePlayer,
    FidePlayerDetail,
    FidePlayerGameStats,
    FidePlayerID,
    FidePlayerRating,
    URLInfo
)
from python_fide.parsing.profile_parsing import (
    profile_charts_parsing,
    profile_detail_parsing,
    profile_stats_parsing
)
from python_fide.constants.common import (
    FIDE_PROFILE_CHARTS_URL,
    FIDE_PROFILE_STATS_URL,
    FIDE_RATINGS_HEADERS
)
from python_fide.endpoint.profile_endpoint import (
    ProfileChartsConfig,
    ProfileDetailConfig,
    ProfileStatsConfig
)

FIDE_CHARTS_INFO = URLInfo(
    url=FIDE_PROFILE_CHARTS_URL, headers=FIDE_RATINGS_HEADERS
)

FIDE_STATS_INFO = URLInfo(
    url=FIDE_PROFILE_STATS_URL, headers=FIDE_RATINGS_HEADERS
)

def _consolidate_fide_player(
    fide_player: Union[FidePlayer, FidePlayerID]
) -> FidePlayer:
    """
    """
    if isinstance(fide_player, FidePlayerID):
        fide_player = get_fide_player(query=fide_player)

        if fide_player is None:
            raise InvalidFideIDError()
    return fide_player


def get_profile_detail(
    fide_player: Union[FidePlayer, FidePlayerID] 
) -> Optional[FidePlayerDetail]:
    """
    """
    config = ProfileDetailConfig(fide_player=fide_player)

    # Request from API to get profile detail JSON response
    response = fide_request(
        url_info=URLInfo(
            url=config.endpointize, headers=FIDE_RATINGS_HEADERS
        )
    )

    # Validate and parse profile detail fields from response
    player_detail = profile_detail_parsing(
        response=response
    )

    # If the ID from the found Fide player does not match the
    # Fide ID passed in as an argument, then return None
    if (
        player_detail is not None and
        player_detail.player.player_id != config.fide_player
    ):
        return
    return player_detail


def get_profile_rating_progress_chart(
    fide_player: Union[FidePlayer, FidePlayerID],
    period: Optional[Period] = None
) -> List[FidePlayerRating]:
    """
    """
    config = ProfileChartsConfig(
        fide_player=fide_player, period=period
    )

    # Request from API to get charts JSON response
    response = fide_request(
        params=config.parameterize, url_info=FIDE_CHARTS_INFO
    )

    # Request from API to get player JSON response
    fide_player = _consolidate_fide_player(
        fide_player=fide_player
    )

    # Validate and parse ratings chart fields from response
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
    config = ProfileStatsConfig(
        fide_player=fide_player,
        fide_player_opponent=fide_player_opponent
    )

    # Request from API to get game stats JSON response
    response = fide_request(
        params=config.parameterize, url_info=FIDE_STATS_INFO,
    )

    # Retrieve the player structure for both the player
    # and the opponent
    fide_player = _consolidate_fide_player(
        fide_player=fide_player
    )
    fide_player_opponent = _consolidate_fide_player(
        fide_player=fide_player_opponent
    )

    # Validate and parse game statistics from response
    game_stats = profile_stats_parsing(
        fide_player=fide_player,
        fide_player_opponent=fide_player_opponent,
        response=response
    )
    return game_stats