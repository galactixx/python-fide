import prettyprinter as pp
from python_fide.clients.event import FideEvents
from python_fide.enums import RatingCategory
from python_fide.types import (
    FideEvent,
    FideEventID,
    FidePlayerName,
    FidePlayerID
)

pp.install_extras(include=['dataclasses'])

client = FideEvents()

event = client.get_event_detail(
    fide_event=FideEventID(entity_id='24687')
)

print(event)