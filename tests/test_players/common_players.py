from typing import List

from python_fide import (
    Date,
    FideGames,
    FideGamesSet,
    FidePlayer,
    FidePlayerBasic,
    FidePlayerDetail,
    FidePlayerGameStats,
    FidePlayerID,
    FidePlayerRating,
    FideRating
)

def game_stats_assertion(game_stats: FidePlayerGameStats) -> None:
    """"""
    assert isinstance(game_stats, FidePlayerGameStats)

    assert game_stats == FidePlayerGameStats(
        player=FIDE_PLAYER_DETAIL_CARLSEN.player,
        opponent=None,
        white=FideGamesSet(
            standard=FideGames(
                games_total=537, games_won=258, games_draw=238, games_lost=41
            ),
            rapid=FideGames(
                games_total=172, games_won=93, games_draw=61, games_lost=18
            ),
            blitz=FideGames(
                games_total=266, games_won=156, games_draw=74, games_lost=36
            )
        ),
        black=FideGamesSet(
            standard=FideGames(
                games_total=524, games_won=131, games_draw=345, games_lost=48
            ),
            rapid=FideGames(
                games_total=170, games_won=70, games_draw=78, games_lost=22
            ),
            blitz=FideGames(
                games_total=269, games_won=137, games_draw=89, games_lost=43
            )  
        )
    )


def rating_chart_assertion(historical_ratings: List[FidePlayerRating]) -> None:
    """"""
    assert len(historical_ratings) == 3
    assert all(
        isinstance(rating, FidePlayerRating) for rating in historical_ratings
    )

    assert historical_ratings[0] == FidePlayerRating(
        month=Date.from_date_format(date='2024-Jan', date_format='%Y-%b'),
        player=FIDE_PLAYER_DETAIL_CARLSEN.player,
        standard=FideRating(games=0, rating=2830),
        rapid=FideRating(games=43, rating=2823),
        blitz=FideRating(games=21, rating=2886)
    )
    assert historical_ratings[1] == FidePlayerRating(
        month=Date.from_date_format(date='2024-Feb', date_format='%Y-%b'),
        player=FIDE_PLAYER_DETAIL_CARLSEN.player,
        standard=FideRating(games=0, rating=2830),
        rapid=FideRating(games=0, rating=2823),
        blitz=FideRating(games=0, rating=2886)
    )
    assert historical_ratings[2] == FidePlayerRating(
        month=Date.from_date_format(date='2024-Mar', date_format='%Y-%b'),
        player=FIDE_PLAYER_DETAIL_CARLSEN.player,
        standard=FideRating(games=0, rating=2830),
        rapid=FideRating(games=0, rating=2823),
        blitz=FideRating(games=0, rating=2886)
    )


def opponents_assertion(opponents: List[FidePlayerBasic]) -> None:
    """"""
    assert len(opponents) == 3
    assert all(
        isinstance(opponent, FidePlayerBasic) for opponent in opponents
    )
    assert opponents[0] == FidePlayerBasic(
        name='Nijat Abasov',
        player_id=13402960,
        country='AZE',
        first_name='Nijat',
        last_name='Abasov'
    )
    assert opponents[1] == FidePlayerBasic(
        name='Nodirbek Abdusattorov',
        player_id=14204118,
        country='UZB',
        first_name='Nodirbek',
        last_name='Abdusattorov'
    )
    assert opponents[2] == FidePlayerBasic(
        name='Michael Adams',
        player_id=400041,
        country='ENG',
        first_name='Michael',
        last_name='Adams'
    )

FIDE_PLAYER_DETAIL_CARLSEN = FidePlayerDetail(
    sex='M',
    birth_year=Date.from_date_format(date='1990', date_format='%Y'),
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

FIDE_PLAYER_DETAIL_NAKAMURA = FidePlayerDetail(
    sex='M',
    birth_year=Date.from_date_format(date='1987', date_format='%Y'),
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

FIDE_PLAYER_PARAMETERS_CARLSEN = [
    FidePlayerID(entity_id='1503014'),
    FidePlayerID(entity_id=1503014),
    FIDE_PLAYER_DETAIL_CARLSEN.player
]

FIDE_PLAYER_PARAMETERS_NAKAMURA = [
    FidePlayerID(entity_id='2016192'),
    FidePlayerID(entity_id=2016192),
    FIDE_PLAYER_DETAIL_NAKAMURA.player
]