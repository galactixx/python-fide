from dataclasses import dataclass
from typing import Optional, Union

import pytest

from python_fide import FidePlayerID
from python_fide.utils._config import parse_fide_player, parse_fide_player_optional
from python_fide.utils._general import build_url, validate_date_format


@dataclass
class CaseParseFidePlayer:
    fide_id: Optional[FidePlayerID]
    exp_id: int


@pytest.mark.parametrize(
    "test_case",
    [
        CaseParseFidePlayer(fide_id=FidePlayerID(fide_id="12222"), exp_id=12222),
        CaseParseFidePlayer(fide_id=FidePlayerID(fide_id=12222), exp_id=12222),
        CaseParseFidePlayer(fide_id=FidePlayerID(fide_id=10006), exp_id=10006),
    ],
)
def test_parse_fide_player(test_case: CaseParseFidePlayer) -> None:
    """Testing the 'parse_fide_player' utility function."""
    assert parse_fide_player(fide_player=test_case.fide_id) == test_case.exp_id


@pytest.mark.parametrize(
    "test_case",
    [
        CaseParseFidePlayer(fide_id=FidePlayerID(fide_id="55332"), exp_id=55332),
        CaseParseFidePlayer(fide_id=FidePlayerID(fide_id=78332), exp_id=78332),
        CaseParseFidePlayer(fide_id=None, exp_id=None),
    ],
)
def test_parse_fide_player_optional(test_case: CaseParseFidePlayer) -> None:
    """Testing the 'parse_fide_player_optional' utility function."""
    assert parse_fide_player_optional(fide_player=test_case.fide_id) == test_case.exp_id


@dataclass
class CaseBuildURL:
    base_url: str
    segments: Union[str, int]
    exp_url: str


@pytest.mark.parametrize(
    "test_case",
    [
        CaseBuildURL(
            base_url="https://fide.com/calendar/",
            segments="53932",
            exp_url="https://fide.com/calendar/53932",
        ),
        CaseBuildURL(
            base_url="https://fide.com/calendar/",
            segments=53932,
            exp_url="https://fide.com/calendar/53932",
        ),
        CaseBuildURL(
            base_url="https://fide.com/calendar/",
            segments="54198",
            exp_url="https://fide.com/calendar/54198",
        ),
    ],
)
def test_build_url(test_case: CaseBuildURL) -> None:
    """Testing the 'build_url' utility function."""
    assert (
        build_url(base=test_case.base_url, segments=test_case.segments)
        == test_case.exp_url
    )


@dataclass
class CaseValidateDateFormat:
    date: str
    date_format: str
    exp_date: str


@pytest.mark.parametrize(
    "test_case",
    [
        CaseValidateDateFormat(
            date="2024-04-01 12:03:00",
            date_format="%Y-%m-%d %H:%M:%S",
            exp_date="2024-04-01",
        ),
        CaseValidateDateFormat(date="1987", date_format="%Y", exp_date="1987-01-01"),
        CaseValidateDateFormat(
            date="2024-Feb", date_format="%Y-%b", exp_date="2024-02-01"
        ),
    ],
)
def test_validate_date_format(test_case: CaseValidateDateFormat) -> None:
    """Testing the 'validate_date_format' utility function."""
    assert (
        validate_date_format(date=test_case.date, date_format=test_case.date_format)
        == test_case.exp_date
    )
