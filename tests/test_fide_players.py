from typing import Any, Dict, Union
from unittest import mock
import pytest

from python_fide import (
    Date,
    FideGames,
    FideGamesSet,
    FidePlayer,
    FidePlayerBasic,
    FidePlayerClient,
    FidePlayerDetail,
    FidePlayerGameStats,
    FidePlayerID,
    FidePlayerRating,
    FideRating,
    Period,
    InvalidFideIDError
)

from python_fide.parsing.player_parsing import player_detail_parsing
from tests.utils import (
    load_json_file,
    MockedResponse
)

fide_player_client = FidePlayerClient()

FIDE_PLAYER_DETAIL_CARLSEN = FidePlayerDetail(
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

FIDE_PLAYER_DETAIL_NAKAMURA = FidePlayerDetail(
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

def test_player_detail_parsing() -> None:
    """
    """
    fide_response_one: Dict[str, Any] = load_json_file(filename='fide_player_carlsen.json')
    player_detail: FidePlayerDetail = player_detail_parsing(response=fide_response_one)
    assert player_detail == FIDE_PLAYER_DETAIL_CARLSEN

    fide_response_one: Dict[str, Any] = load_json_file(filename='fide_player_nakamura.json')
    player_detail: FidePlayerDetail = player_detail_parsing(response=fide_response_one)
    assert player_detail == FIDE_PLAYER_DETAIL_NAKAMURA


@pytest.mark.parametrize(
    'fide_player', [
        FidePlayerID(entity_id='1503014'),
        FidePlayerID(entity_id=1503014),
        FIDE_PLAYER_DETAIL_CARLSEN.player
    ]
)
@mock.patch(
    target='requests.get',
    side_effect=MockedResponse(filename='fide_player_carlsen.json').mock_response,
    autospec=True
)
def test_player_mock_detail_carslen(_, fide_player: Union[FidePlayer, FidePlayerID]) -> None:
    """
    """
    player_detail: FidePlayerDetail = fide_player_client.get_fide_player_detail(
        fide_player=fide_player
    )
    assert player_detail == FIDE_PLAYER_DETAIL_CARLSEN


@pytest.mark.parametrize(
    'fide_player', [
        FidePlayerID(entity_id='2016192'),
        FidePlayerID(entity_id=2016192),
        FIDE_PLAYER_DETAIL_NAKAMURA.player
    ]
)
@mock.patch(
    target='requests.get',
    side_effect=MockedResponse(filename='fide_player_nakamura.json').mock_response,
    autospec=True
)
def test_player_mock_detail_nakamura(_, fide_player: Union[FidePlayer, FidePlayerID]) -> None:
    """
    """
    player_detail: FidePlayerDetail = fide_player_client.get_fide_player_detail(
        fide_player=fide_player
    )
    assert player_detail == FIDE_PLAYER_DETAIL_NAKAMURA


@mock.patch(
    target='requests.get',
    side_effect=MockedResponse(filename='fide_opponents.json').mock_response,
    autospec=True
)
def test_player_mock_opponents(_) -> None:
    """
    """
    opponents = fide_player_client.get_fide_player_opponents(
        fide_player=FIDE_PLAYER_DETAIL_CARLSEN.player
    )

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


@mock.patch(
    target='requests.get',
    side_effect=MockedResponse(filename='fide_rating_chart.json').mock_response,
    autospec=True
)
def test_player_mock_rating_progress_chart(_) -> None:
    """
    """
    historical_ratings = fide_player_client.get_fide_player_rating_progress_chart(
        period=Period.ONE_YEAR, fide_player=FIDE_PLAYER_DETAIL_CARLSEN.player
    )

    assert len(historical_ratings) == 3
    assert all(
        isinstance(rating, FidePlayerRating) for rating in historical_ratings
    )

    assert historical_ratings[0] == FidePlayerRating(
        month=Date(
            date_iso='2024-01-01', date_original='2024-Jan', date_original_format='%Y-%b'
        ),
        player=FIDE_PLAYER_DETAIL_CARLSEN.player,
        standard=FideRating(games=0, rating=2830),
        rapid=FideRating(games=43, rating=2823),
        blitz=FideRating(games=21, rating=2886)
    )
    assert historical_ratings[1] == FidePlayerRating(
        month=Date(
            date_iso='2024-02-01', date_original='2024-Feb', date_original_format='%Y-%b'
        ),
        player=FIDE_PLAYER_DETAIL_CARLSEN.player,
        standard=FideRating(games=0, rating=2830),
        rapid=FideRating(games=0, rating=2823),
        blitz=FideRating(games=0, rating=2886)
    )
    assert historical_ratings[2] == FidePlayerRating(
        month=Date(
            date_iso='2024-03-01', date_original='2024-Mar', date_original_format='%Y-%b'
        ),
        player=FIDE_PLAYER_DETAIL_CARLSEN.player,
        standard=FideRating(games=0, rating=2830),
        rapid=FideRating(games=0, rating=2823),
        blitz=FideRating(games=0, rating=2886)
    )


@mock.patch(
    target='requests.get',
    side_effect=MockedResponse(filename='fide_game_stats.json').mock_response,
    autospec=True
)
def test_player_mock_game_stats(_) -> None:
    """
    """
    game_stats = fide_player_client.get_fide_player_game_stats(
        fide_player=FIDE_PLAYER_DETAIL_CARLSEN.player
    )

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
    

@pytest.mark.parametrize(
    'fide_player_id, error', [
        ('H19JF433', 'invalid Fide ID entered, must be an integer (as str in int type)'),
        ('0023FFH8', 'invalid Fide ID entered, must be an integer (as str in int type)'),
        ('003953322', 'invalid Fide ID entered, cannot start with a zero')
    ]
)
def test_player_error_invalid_fide_id(fide_player_id: str, error: str) -> None:
    """
    """
    with pytest.raises(InvalidFideIDError) as exc_info:
        _ = FidePlayerID(entity_id=fide_player_id)
    assert str(exc_info.value) == error