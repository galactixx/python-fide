from typing import List

from python_fide.types import (
    FidePlayerRating,
    FidePlayerGameStats,
    _FidePlayerGameStatsRaw
)

def profile_charts_parsing(response: List[dict]) -> List[FidePlayerRating]:
    gathered_ratings: List[FidePlayerRating] = []
    for month_rating in response:
        fide_rating = FidePlayerRating.model_validate(month_rating)
        gathered_ratings.append(fide_rating)

    return gathered_ratings


def profile_stats_parsing(response: List[dict]) -> FidePlayerGameStats:
    if not isinstance(response, list) and len(response) != 1:
        raise ValueError(
            "expecting response to be a list with a singular dictionary"
        )

    raw_stats = _FidePlayerGameStatsRaw.model_validate(
        response[0]
    )

    complete_stats = raw_stats.to_complete_stats()
    return complete_stats