from typing import List, Optional

from python_fide.exceptions import InvalidFormatError
from python_fide.types.adapters import PartialListAdapter
from python_fide.types.core import (
    FidePlayer,
    FidePlayerBasic,
    FidePlayerDetail,
    FidePlayerGameStats,
    FidePlayerRating
)

def player_opponents_parsing(response: List[dict]) -> List[FidePlayerBasic]:
    """
    Logic to parse the response returned from the opponents
    endpoint.

    Args:
        response (List[dict]): A list of dictionaries each
            representing a Fide player.

    Returns:
        List[FidePlayerBasic]: A list of FidePlayerBasic objects
            each representing an opponent the player in question
            has faced.
    """
    players = PartialListAdapter.from_minimal_adapter(response=response)
    gathered_players: List[FidePlayerBasic] = []
    
    for player in players.data:
        fide_player = FidePlayerBasic.from_validated_model(player=player)
        gathered_players.append(fide_player)
    
    return gathered_players


def player_detail_parsing(response: List[dict]) -> Optional[FidePlayerDetail]:
    """
    Logic to parse the response returned from the player
    detail endpoint.

    Args:
        response (List[dict]): A list of dictionaries. In
            this case, if the Fide ID is valid, there should
            only be one dictionary in the list.

    Returns:
        FidePlayerDetail | None: A FidePlayerDetail object or
            if the Fide player ID is invalid, None.
    """
    players = PartialListAdapter.from_minimal_adapter(response=response)

    # This is a search by Fide ID, thus there should never
    # be a response that has more than one item, although
    # there can be a response with no items
    if players.num_observations == 1:
        fide_detail = FidePlayerDetail.from_validated_model(
            player=players.extract
        )
        return fide_detail
    elif players.num_observations == 0:
        return
    else:
        raise InvalidFormatError(
            "invalid format, a player detail response cannot return more than one player"
        )


def player_charts_parsing(
    fide_player: FidePlayer, response: List[dict]
) -> List[FidePlayerRating]:
    """
    Logic to parse the response returned from the player
    ratings endpoint.

    Args:
        fide_player (FidePlayer): A FidePlayer object.
        response (List[dict]): A list of dictionaries each
            representing a set of ratings for a specific month.

    Returns:
        List[FidePlayerRating]: A list of FidePlayerRating objects,
            each reprsenting a set of ratings for a specific month.
    """
    ratings = PartialListAdapter.from_minimal_adapter(response=response)
    gathered_ratings: List[FidePlayerRating] = []

    for month_rating in ratings.data:
        fide_rating = FidePlayerRating.from_validated_model(
            player=fide_player, rating=month_rating
        )
        gathered_ratings.append(fide_rating)

    return gathered_ratings


def player_stats_parsing(
    fide_player: FidePlayer,
    fide_player_opponent: Optional[FidePlayer],
    response: List[dict]
) -> FidePlayerGameStats:
    """
    Logic to parse the response returned from the game stats
    endpoint.

    Args:
        fide_player (FidePlayer): A FidePlayer object representing
            the player in question.
        fide_player_opponent (FidePlayer | None): A FidePlayer
            object representing the opponent, otherwise None.
        response (List[dict]): A list of dictionaries. In this case,
            there should only ever be one dictionary in the list.

    Returns:
        FidePlayerGameStats: A FidePlayerGameStats object consisting
            of game statistics for the given Fide player.
    """
    player_stats = PartialListAdapter.from_minimal_adapter(response=response)

    # This is a search by Fide ID, thus there should never
    # be a response that has more than one item, although there
    # can be a response with no items
    if player_stats.num_observations == 1:
        fide_stats = FidePlayerGameStats.from_validated_model(
            fide_player=fide_player,
            fide_player_opponent=fide_player_opponent,
            stats=player_stats.extract
        )
        return fide_stats
    else:
        raise InvalidFormatError(
            "invalid format, a stats response should always return only one set of stats"
        )