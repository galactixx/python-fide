import prettyprinter as pp
from python_fide.clients.player import FidePlayerData
from python_fide.enums import RatingCategory
from python_fide.types.core import (
    FideEvent,
    FideEventID,
    FidePlayerName,
    FidePlayerID
)

pp.install_extras(include=['dataclasses'])

client = FidePlayerData()

entity = client.get_fide_player_detail(
    fide_player=FidePlayerID(entity_id='1700880')
)

print(entity)