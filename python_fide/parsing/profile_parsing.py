from typing import List, Optional

from python_fide.types import (
    FidePlayer,
    FidePlayerDetail,
    FidePlayerGameStats,
    FidePlayerRating
)

def profile_detail_parsing(response: List[dict]) -> Optional[FidePlayerDetail]:
    """
    """
    # This is a search by Fide ID, thus there should never be a response
    # that has more than one item, although there can be a response with no items
    if len(response) > 1:
        raise ValueError(
            "a player detail response cannot have more than one result"
        )
    elif len(response) == 0:
        return
    else:
        fide_detail = FidePlayerDetail.from_validated_model(
            player=response[0]
        )
        return fide_detail


def profile_charts_parsing(
    fide_player: FidePlayer,
    response: List[dict]
) -> List[FidePlayerRating]:
    """
    """
    gathered_ratings: List[FidePlayerRating] = []
    for month_rating in response:
        fide_rating = FidePlayerRating.from_validated_model(
            player=fide_player,
            rating=month_rating
        )
        gathered_ratings.append(fide_rating)

    return gathered_ratings


def profile_stats_parsing(
    fide_player: FidePlayer,
    fide_player_opponent: Optional[FidePlayer],
    response: List[dict]
) -> FidePlayerGameStats:
    """
    """
    # If a player exists in the Fide database then there should always
    # be a non-null response returned
    if len(response) != 1:
        raise ValueError(
            "expecting response to be a list with a singular dictionary"
        )

    fide_stats = FidePlayerGameStats.from_validated_model(
        fide_player=fide_player,
        fide_player_opponent=fide_player_opponent,
        stats=response[0]
    )

    return fide_stats