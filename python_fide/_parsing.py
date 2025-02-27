from typing import List, Optional

from python_fide._exceptions import InvalidFormatError
from python_fide._typing import FidePlayerLike
from python_fide.types._adapters import PartialListAdapter
from python_fide.types._core import FidePlayer, FidePlayerGameStats, FidePlayerRating
from python_fide.utils._config import to_fide_id, to_fide_id_optional


def player_opponents_parsing(response: List[dict]) -> List[FidePlayer]:
    """
    Logic to parse the response returned from the opponents
    endpoint.
    """
    players = PartialListAdapter.from_minimal_adapter(response=response)
    gathered_players: List[FidePlayer] = []

    for player in players.data:
        fide_player = FidePlayer.model_validate(player)
        gathered_players.append(fide_player)

    return gathered_players


def player_charts_parsing(
    player: FidePlayerLike, response: List[dict]
) -> List[FidePlayerRating]:
    """
    Logic to parse the response returned from the player
    ratings endpoint.
    """
    fide_id = to_fide_id(fide_player=player)
    ratings = PartialListAdapter.from_minimal_adapter(response=response)
    gathered_ratings: List[FidePlayerRating] = []

    for month_rating in ratings.data:
        fide_rating = FidePlayerRating.from_validated_model(
            fide_id=fide_id, rating=month_rating
        )
        gathered_ratings.append(fide_rating)

    return gathered_ratings


def player_stats_parsing(
    player: FidePlayerLike,
    opponent: Optional[FidePlayerLike],
    response: List[dict],
) -> FidePlayerGameStats:
    """
    Logic to parse the response returned from the game stats
    endpoint.
    """
    player_stats = PartialListAdapter.from_minimal_adapter(response=response)

    # This is a search by Fide ID, thus there should never
    # be a response that has more than one item, although there
    # can be a response with no items
    if player_stats.num_observations == 1:
        fide_id = to_fide_id(fide_player=player)
        fide_id_opponent = to_fide_id_optional(fide_player=opponent)
        fide_stats = FidePlayerGameStats.from_validated_model(
            fide_id=fide_id,
            fide_id_opponent=fide_id_opponent,
            stats=player_stats.extract,
        )
        return fide_stats
    else:
        raise InvalidFormatError(
            "Invalid format, a stats response should always return only one set of stats"
        )
