from python_fide import (
    Date,
    FideEvent,
    FideEventDetail
)

FIDE_EVENT_DETAIL_53626 = FideEventDetail(
    event=FideEvent(name='Candidates Tournament', event_id=53626),
    city='Toronto',
    country='Canada',
    start_date=Date(
        date_iso='2024-04-03',
        date_original='2024-04-03 00:00:00',
        date_original_format='%Y-%m-%d %H:%M:%S'
    ),
    end_date=Date(
        date_iso='2024-04-23', 
        date_original='2024-04-23 23:59:59',
        date_original_format='%Y-%m-%d %H:%M:%S'
    ),
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
    chief_organizer=None
)

FIDE_EVENT_DETAIL_53627 = FideEventDetail(
    event=FideEvent(name="Women's Candidates Tournament", event_id=53627),
    city='Toronto',
    country='Canada',
    start_date=Date(
        date_iso='2024-04-03',
        date_original='2024-04-03 00:00:00',
        date_original_format='%Y-%m-%d %H:%M:%S'
    ),
    end_date=Date(
        date_iso='2024-04-23',
        date_original='2024-04-23 23:59:59',
        date_original_format='%Y-%m-%d %H:%M:%S'
    ),
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
    chief_organizer=None
)