import prettyprinter as pp
from python_fide.clients.top_players import TopPlayer
from python_fide.enums import RatingCategory

pp.install_extras(include=['dataclasses'])

event_client = TopPlayer()

events = event_client.get_top_standard_players(
    limit=10,
    categories=[RatingCategory.OPEN]
)

pp.pprint(
    events[0]
)

print('*****************************')
print('*****************************')
pp.pprint(
    events[-1]
)