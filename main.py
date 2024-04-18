import prettyprinter as pp
from python_fide.clients.top_players import FideTopPlayer
from python_fide.types import FidePlayerName, FidePlayerID
from python_fide.enums import RatingCategory

pp.install_extras(include=['dataclasses'])

client = FideTopPlayer()

players = client.get_top_standard_players(
    limit=2,
    categories=[RatingCategory.OPEN]
)

print(players)