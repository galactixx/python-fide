from typing import List, Optional

from python_fide.clients.fide_client import FideClient
from python_fide.constants.periods import Period
from python_fide.types import (
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
    fide_id: FidePlayerID,
    period: Optional[Period] = None
) -> List[FidePlayerRating]:
    """
    """
    with FideClient() as session:
        config = ProfileChartsConfig(
            fide_id=fide_id, period=period
        )

        response = session.request(
            params=config.parameterize,
            url_info=FIDE_CHARTS_INFO
        )

        rating_charts = profile_charts_parsing(
            response=response
        )
        return rating_charts


def get_profile_game_stats(
    fide_id: FidePlayerID, 
    opponent_fide_id: Optional[FidePlayerID] = None
) -> List[FidePlayerGameStats]:
    """
    """
    with FideClient() as session:
        config = ProfileStatsConfig(
            fide_id=fide_id, opponent_fide_id=opponent_fide_id
        )

        response = session.request(
            params=config.parameterize,
            url_info=FIDE_STATS_INFO,
        )

        game_stats = profile_stats_parsing(
            response=response
        )
        return game_stats