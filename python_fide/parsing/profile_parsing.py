from typing import List

from python_fide.types import (
    FidePlayer,
    FidePlayerRating,
    FidePlayerGameStats
)

def profile_charts_parsing(
    fide_player: FidePlayer,
    response: List[dict]
) -> List[FidePlayerRating]:
    gathered_ratings: List[FidePlayerRating] = []
    for month_rating in response:
        fide_rating = FidePlayerRating.from_validated_model(
            player=fide_player,
            rating=month_rating
        )
        gathered_ratings.append(fide_rating)

    return gathered_ratings


def profile_stats_parsing(response: List[dict]) -> FidePlayerGameStats:
    if not isinstance(response, list) and len(response) != 1:
        raise ValueError(
            "expecting response to be a list with a singular dictionary"
        )

    raw_stats = FidePlayerGameStats.from_validated_model(
        response[0]
    )

    complete_stats = raw_stats.to_complete_stats()
    return complete_stats