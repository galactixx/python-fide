import prettyprinter as pp
from python_fide.clients.player import FidePlayerClient
from python_fide.types.core import FidePlayerID

pp.install_extras(include=['dataclasses'])

client = FidePlayerClient()

entity = client.get_fide_player_detail(
    fide_player=FidePlayerID(entity_id='2016192')
)

print(entity)