from typing import Any, Dict, Tuple

from python_fide.types.base import BasePlayer

def from_player_model(
    player: Dict[str, Any],
    fide_player_model: BasePlayer
) -> Tuple[str, str, Dict[str, Any]]:
    """
    """
    fide_player = fide_player_model.model_validate(player)
    first_name, last_name = fide_player.get_decomposed_player_name()
    fide_player.set_player_name(
        first_name=first_name, last_name=last_name
    )

    return (
        first_name, last_name, fide_player.model_dump()
    )