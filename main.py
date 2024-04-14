import prettyprinter as pp
from python_fide.clients.event import FideEvents

pp.install_extras(include=['dataclasses'])

event_client = FideEvents()

pp.pprint(
    event_client.get_latest_events(
        limit=1
    )
)