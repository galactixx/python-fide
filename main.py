import prettyprinter as pp
from python_fide.clients.event import FideEventsClient
from python_fide.types.core import FidePlayerID, FidePlayer, FidePlayerRating
from python_fide.enums import Period

pp.install_extras(include=['dataclasses'])

client = FideEventsClient()

events = client.get_latest_events(
    query='Chess', limit=10
)

print(events)