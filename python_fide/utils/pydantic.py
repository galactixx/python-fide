from typing import Any, Dict, Optional, Tuple

from python_fide.types.base import BasePlayer

def from_player_model(
    player: Dict[str, Any],
    fide_player_model: BasePlayer
) -> Tuple[str, Optional[str], Dict[str, Any]]:
    """
    Given a player API response and a derived model from
    BasePlayer, will validate the model, extract the raw
    player name, and reset the player name after some
    transformation. Finally, the first name, last name, and
    a dictionary representation of the validated model are
    returned.
    
    Args:
        player (Dict[str, Any]): A dictionary representing a
            player.
        fide_player_model (BasePlayer): A player associated
            derived model from BasePlayer.

    Returns:
        Tuple[str, str | None, Dict[str, Any]]: A tuple of the
            first name, last name, and a dictionary representation
            of the validated model.
    """
    fide_player = fide_player_model.model_validate(player)
    first_name, last_name = fide_player._get_decomposed_player_name()
    fide_player._set_player_name(
        first_name=first_name, last_name=last_name
    )

    return (
        first_name, last_name, fide_player.model_dump()
    )