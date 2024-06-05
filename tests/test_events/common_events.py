from python_fide import (
    Date,
    FideEvent,
    FideEventDetail,
    FideEventID
)

FIDE_EVENT_DETAIL_CANDIDATES = FideEventDetail(
    city='Toronto',
    country='Canada',
    start_date=Date.from_date_format(date='2024-04-03 00:00:00', date_format='%Y-%m-%d %H:%M:%S'),
    end_date=Date.from_date_format(date='2024-04-23 23:59:59', date_format='%Y-%m-%d %H:%M:%S'),
    game_format='s',
    tournament_type=None,
    time_control=None,
    time_control_desc=None,
    rounds=None,
    players=None,
    telephone=None,
    website='https://candidates2024.fide.com/',
    organizer=None,
    chief_arbiter=None,
    chief_organizer=None,
    event=FideEvent(name='Candidates Tournament', event_id=53626)
)

FIDE_EVENT_DETAIL_CANDIDATES_WOMEN = FideEventDetail(
    city='Toronto',
    country='Canada',
    start_date=Date.from_date_format(date='2024-04-03 00:00:00', date_format='%Y-%m-%d %H:%M:%S'),
    end_date=Date.from_date_format(date='2024-04-23 23:59:59', date_format='%Y-%m-%d %H:%M:%S'),
    game_format='s',
    tournament_type=None,
    time_control=None,
    time_control_desc=None,
    rounds=None,
    players=None,
    telephone=None,
    website='https://candidates2024.fide.com/',
    organizer=None,
    chief_arbiter=None,
    chief_organizer=None,
    event=FideEvent(name="Women's Candidates Tournament", event_id=53627)
)

FIDE_EVENT_PARAMETERS_CANDIDATES = [
    FideEventID(entity_id='53626'),
    FideEventID(entity_id=53626),
    FIDE_EVENT_DETAIL_CANDIDATES.event
]

FIDE_EVENT_PARAMETERS_CANDIDATES_WOMEN = [
    FideEventID(entity_id='53627'),
    FideEventID(entity_id=53627),
    FIDE_EVENT_DETAIL_CANDIDATES_WOMEN.event
]