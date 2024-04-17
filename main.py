import prettyprinter as pp
from python_fide.clients.search import FideSearch
from python_fide.types import FidePlayerName, FidePlayerID

pp.install_extras(include=['dataclasses'])

client = FideSearch()

players = client.get_fide_players_by_id(
    fide_player_id=FidePlayerID(entity_id='1022')
)

pp.pprint(
    players
)
print(len(players))


# players = client.get_fide_players_by_name(
#     fide_player_name=FidePlayerName(first_name='John', last_name='Smith')
# )

# pp.pprint(
#     players
# )
# print(len(players))