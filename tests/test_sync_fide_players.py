from unittest import mock
from typing import Any

import pytest

from python_fide import FidePlayerID, InvalidFideIDError, Period
from python_fide.clients_sync import FidePlayerClient
from tests.common import (
    game_stats_assertion,
    opponents_assertion,
    rating_chart_assertion,
)
from tests.utils import MockedResponse

fide_player_client = FidePlayerClient()


@mock.patch(
    target="requests.get",
    side_effect=MockedResponse(filename="fide_opponents.json").mock_response,
    autospec=True,
)
def test_player_mock_opponents(_: Any) -> None:
    """Testing the player opponents functionality."""
    opponents = fide_player_client.get_opponents(
        fide_player=FidePlayerID(fide_id=1503014)
    )
    opponents_assertion(opponents=opponents)


@mock.patch(
    target="requests.get",
    side_effect=MockedResponse(filename="fide_rating_chart.json").mock_response,
    autospec=True,
)
def test_player_mock_rating_progress_chart(_: Any) -> None:
    """Testing the player historical ratings functionality."""
    historical_ratings = fide_player_client.get_rating_progress_chart(
        period=Period.ONE_YEAR, fide_id=FidePlayerID(fide_id=1503014)
    )
    rating_chart_assertion(historical_ratings=historical_ratings)


@mock.patch(
    target="requests.get",
    side_effect=MockedResponse(filename="fide_game_stats.json").mock_response,
    autospec=True,
)
def test_player_mock_game_stats(_: Any) -> None:
    """Testing the player game statistics functionality."""
    game_stats = fide_player_client.get_game_stats(
        fide_id=FidePlayerID(fide_id=1503014)
    )
    game_stats_assertion(game_stats=game_stats)


@pytest.mark.parametrize(
    "fide_player_id, error",
    [
        (
            "H19JF433",
            "invalid Fide ID entered, must be an integer (as str in int type)",
        ),
        (
            "0023FFH8",
            "invalid Fide ID entered, must be an integer (as str in int type)",
        ),
        ("003953322", "invalid Fide ID entered, cannot start with a zero"),
    ],
)
def test_player_error_invalid_fide_id(fide_player_id: str, error: str) -> None:
    """Testing the InvalidFideIDError for the FidePlayerID class."""
    with pytest.raises(InvalidFideIDError) as exc_info:
        _ = FidePlayerID(fide_id=fide_player_id)  # type: ignore[arg-type]
    assert str(exc_info.value) == error
