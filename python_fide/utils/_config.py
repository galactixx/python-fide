from typing import Optional

from python_fide._typing import FidePlayerLike
from python_fide.types._core import FidePlayer, FidePlayerID


def to_fide_id(fide_player: FidePlayerLike) -> FidePlayerID:
    """
    Given a `FidePlayer` or `FidePlayerID` object, will return an
    `FidePlayerID` object representing the Fide ID of the player.
    """
    fide_id = parse_fide_player(fide_player=fide_player)
    return FidePlayerID(fide_id=fide_id)


def to_fide_id_optional(
    fide_player: Optional[FidePlayerLike],
) -> Optional[FidePlayerID]:
    """
    Given a `FidePlayer` or `FidePlayerID` object, will return an
    `FidePlayerID` object representing the Fide ID of the player.
    Can be None if no object is passed as an argument.
    """
    fide_id = parse_fide_player_optional(fide_player=fide_player)
    if fide_id is not None:
        return FidePlayerID(fide_id=fide_id)
    else:
        return None


def parse_fide_player(fide_player: FidePlayerLike) -> int:
    """
    Given a `FidePlayer` or `FidePlayerID` object, will return an
    integer representing the Fide ID of the player.
    """
    if isinstance(fide_player, FidePlayer):
        return fide_player.fide_id
    elif isinstance(fide_player, FidePlayerID):
        return fide_player.fide_id
    else:
        raise ValueError("not a valid 'fide_player' type")


def parse_fide_player_optional(fide_player: Optional[FidePlayerLike]) -> Optional[int]:
    """
    Given a `FidePlayer` or `FidePlayerID` object, will return an
    integer representing the Fide ID of the player. If no
    fide_player is specified, will return None.
    """
    if fide_player is not None:
        return parse_fide_player(fide_player=fide_player)
    else:
        return
