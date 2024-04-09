from typing import List, Optional, Union

from python_fide.clients.base_client import BaseClient
from python_fide.constants.periods import Period
from python_fide.types import (
    FidePlayerGameStats,
    FidePlayerRating
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

class ProfileClient(BaseClient):
    """
    """
    def __init__(self):
        super().__init__()

    def get_ratings(
        self,
        fide_id: Union[str, int],
        period: Optional[Period] = None
    ) -> List[FidePlayerRating]:
        config = ProfileChartsConfig(
            fide_id=fide_id, period=period
        )

        response = self._fide_request(
            fide_url=FIDE_PROFILE_CHARTS_URL,
            params=config.parameterize,
            headers=FIDE_RATINGS_HEADERS
        )

        return profile_charts_parsing(
            response=response
        )

    def get_results_statistics(
        self,
        fide_id: Union[str, int], 
        opponent_fide_id: Optional[Union[str, int]] = None
    ) -> List[FidePlayerGameStats]:
        config = ProfileStatsConfig(
            fide_id=fide_id, opponent_fide_id=opponent_fide_id
        )

        response = self._fide_request(
            fide_url=FIDE_PROFILE_STATS_URL,
            params=config.parameterize,
            headers=FIDE_RATINGS_HEADERS
        )

        return profile_stats_parsing(
            response=response
        )