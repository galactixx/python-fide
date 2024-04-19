import prettyprinter as pp
from python_fide.clients.event import FideEventsClient
from python_fide.enums import RatingCategory
from python_fide.types.core import (
    FideEvent,
    FideEventID,
    FidePlayerName,
    FidePlayerID
)

pp.install_extras(include=['dataclasses'])

client = FideEventsClient()

entity = client.get_event_detail(
    fide_event=FideEventID(entity_id=53627)
)

pp.pprint(entity)