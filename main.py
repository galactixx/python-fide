# from python_fide.clients.search_client import FideSearchClient

# client = FideSearchClient()

# events = client.get_news(
#     query='world cadet', limit=100
# )

# print(len(events))
# print(events[0].news_url)

import prettyprinter as pp
from python_fide.clients.profile import get_profile_rating_progress_chart
from python_fide.types import FidePlayerID

pp.install_extras(include=['dataclasses'])

pp.pprint(
    get_profile_rating_progress_chart(
        fide_player=FidePlayerID(entity_id='1700880')
    )[0]
)