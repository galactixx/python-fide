from typing import List

from python_fide import (
    Date,
    FideGames,
    FideGamesSet,
    FidePlayer,
    FidePlayerGameStats,
    FidePlayerRating,
    FideRating,
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
            ),
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
            ),
        ),
    )


def rating_chart_assertion(historical_ratings: List[FidePlayerRating]) -> None:
    """"""
    assert len(historical_ratings) == 3
    assert all(isinstance(rating, FidePlayerRating) for rating in historical_ratings)

    assert historical_ratings[0] == FidePlayerRating(
        month=Date.from_date_format(date="2024-Jan", date_format="%Y-%b"),
        player=FIDE_PLAYER_DETAIL_CARLSEN.player,
        standard=FideRating(games=0, rating=2830),
        rapid=FideRating(games=43, rating=2823),
        blitz=FideRating(games=21, rating=2886),
    )
    assert historical_ratings[1] == FidePlayerRating(
        month=Date.from_date_format(date="2024-Feb", date_format="%Y-%b"),
        player=FIDE_PLAYER_DETAIL_CARLSEN.player,
        standard=FideRating(games=0, rating=2830),
        rapid=FideRating(games=0, rating=2823),
        blitz=FideRating(games=0, rating=2886),
    )
    assert historical_ratings[2] == FidePlayerRating(
        month=Date.from_date_format(date="2024-Mar", date_format="%Y-%b"),
        player=FIDE_PLAYER_DETAIL_CARLSEN.player,
        standard=FideRating(games=0, rating=2830),
        rapid=FideRating(games=0, rating=2823),
        blitz=FideRating(games=0, rating=2886),
    )


def opponents_assertion(opponents: List[FidePlayer]) -> None:
    """"""
    assert len(opponents) == 3
    assert all(isinstance(opponent, FidePlayer) for opponent in opponents)
    assert opponents[0] == FidePlayer(
        name="Nijat Abasov",
        player_id=13402960,
        country="AZE",
    )
    assert opponents[1] == FidePlayer(
        name="Nodirbek Abdusattorov", player_id=14204118, country="UZB"
    )
    assert opponents[2] == FidePlayer(
        name="Michael Adams",
        player_id=400041,
        country="ENG",
    )
