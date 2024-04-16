from typing import List, Optional

from python_fide.exceptions import InvalidFormatError
from python_fide.types import (
    FidePlayer,
    FidePlayerBasic,
    FidePlayerDetail,
    FidePlayerGameStats,
    FidePlayerRating
)

def player_opponents_parsing(response: List[dict]) -> List[FidePlayerBasic]:
    """
    """
    gathered_players: List[FidePlayerBasic] = []
    
    for player in response:
        fide_player = FidePlayerBasic.from_validated_model(player=player)
        gathered_players.append(fide_player)
    
    return gathered_players


def player_detail_parsing(response: List[dict]) -> Optional[FidePlayerDetail]:
    """
    """
    if not isinstance(response, list):
        raise InvalidFormatError()

    num_players_returned = len(response)

    # This is a search by Fide ID, thus there should never be a response
    # that has more than one item, although there can be a response with no items
    if num_players_returned == 1:
        fide_detail = FidePlayerDetail.from_validated_model(
            player=response[0]
        )
        return fide_detail
    elif num_players_returned == 0:
        return
    else:
        raise InvalidFormatError(
            "invalid format, a player detail response cannot return more than one player"
        )


def player_charts_parsing(
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


def player_stats_parsing(
    fide_player: FidePlayer,
    fide_player_opponent: Optional[FidePlayer],
    response: List[dict]
) -> FidePlayerGameStats:
    """
    """
    num_stats_returned = len(response)

    # This is a search by Fide ID, thus there should never be a response
    # that has more than one item, although there can be a response with no items
    if num_stats_returned == 1:
        fide_stats = FidePlayerGameStats.from_validated_model(
            fide_player=fide_player,
            fide_player_opponent=fide_player_opponent,
            stats=response[0]
        )
        return fide_stats
    else:
        raise InvalidFormatError(
            "invalid format, a stats response should always return only one set of stats"
        )