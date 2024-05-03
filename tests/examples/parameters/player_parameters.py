from python_fide import (
    Date,
    FidePlayer,
    FidePlayerDetail
)

FIDE_PLAYER_DETAIL_1503014 = FidePlayerDetail(
    sex='M',
    birth_year=Date(
        date_iso='1990-01-01', date_original='1990', date_original_format='%Y'
    ),
    rating_standard=2830,
    rating_rapid=2828,
    rating_blitz=2886,
    player=FidePlayer(
        name='Magnus Carlsen',
        player_id=1503014, 
        title='GM', 
        country='NOR', 
        first_name='Magnus', 
        last_name='Carlsen'
    )
)

FIDE_PLAYER_DETAIL_2016192 = FidePlayerDetail(
    sex='M',
    birth_year=Date(
        date_iso='1987-01-01', date_original='1987', date_original_format='%Y'
    ),
    rating_standard=2794,
    rating_rapid=2746,
    rating_blitz=2874,
    player=FidePlayer(
        name='Hikaru Nakamura',
        player_id=2016192,
        title='GM',
        country='USA',
        first_name='Hikaru',
        last_name='Nakamura'
    )
)