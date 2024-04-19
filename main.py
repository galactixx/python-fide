import prettyprinter as pp
from python_fide.clients.search import FideSearchClient
from python_fide.enums import RatingCategory
from python_fide.types.core import (
    FideEvent,
    FideEventID,
    FidePlayerName,
    FidePlayerID
)

pp.install_extras(include=['dataclasses'])

client = FideSearchClient()

entity = client.get_news(
    query='Candidates', limit=1
)

print(entity)