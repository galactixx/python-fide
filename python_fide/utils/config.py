from typing import Optional, Union

from python_fide.types.core import (
    FidePlayer,
    FidePlayerID
)

def parse_fide_player(
    fide_player: Union[FidePlayer, FidePlayerID]
) -> int:
    """
    Given a FidePlayer or FidePlayerID object, will return an
    integer representing the Fide ID of the player.

    Args:
        fide_player (FidePlayer | FidePlayerID): A FidePlayer or
            FidePlayerID object.

    Returns:
        int: An integer representing the Fide ID of the player.
    """
    if isinstance(fide_player, FidePlayer):
        return fide_player.player_id
    elif isinstance(fide_player, FidePlayerID):
        return fide_player.entity_id
    else:
        raise ValueError(
            "not a valid 'fide_player' type"
        )
    

def parse_fide_player_optional(
    fide_player: Optional[Union[FidePlayer, FidePlayerID]]
) -> Optional[int]:
    """
    Given a FidePlayer or FidePlayerID object, will return an
    integer representing the Fide ID of the player. If no
    fide_player is specified, will return None.
    
    Args:
        fide_player (FidePlayer | FidePlayerID | None): A
            FidePlayeror FidePlayerID object. Can also be None
            if the argument is not specified.

    Returns:
        int | None: An integer representing the Fide ID of
            the player or None.
    """
    if fide_player is not None:
        return parse_fide_player(fide_player=fide_player)
    else:
        return