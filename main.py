import prettyprinter as pp
from python_fide.clients.player import FidePlayerClient
from python_fide.types.core import FidePlayerID, FidePlayer, FidePlayerRating
from python_fide.enums import Period

pp.install_extras(include=['dataclasses'])

client = FidePlayerClient()

historical_ratings = client.get_fide_player_rating_progress_chart(
    period=Period.ONE_YEAR, fide_player=FidePlayerID(entity_id='1503014')
)

print(historical_ratings)