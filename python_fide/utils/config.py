from typing import Optional, Union

from python_fide.types.core import (
    FidePlayer,
    FidePlayerID
)

def parse_fide_player(
    fide_player: Union[FidePlayer, FidePlayerID]
) -> int:
    """
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
    """
    if fide_player is not None:
        return parse_fide_player(fide_player=fide_player)
    else:
        return