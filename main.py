import prettyprinter as pp
from python_fide.clients.event import get_event_detail
from python_fide.types import FideEventID

pp.install_extras(include=['dataclasses'])

pp.pprint(
    get_event_detail(
        fide_event=FideEventID(entity_id='54155')
    )
)