from typing import Any, Dict, Optional, Union
from dataclasses import dataclass

import pytest
from python_fide import FidePlayerID

from python_fide.types.base import FidePlayerRaw
from python_fide.utils.pydantic import from_player_model
from python_fide.utils.config import (
    parse_fide_player,
    parse_fide_player_optional
)
from python_fide.utils.general import (
    build_url,
    clean_fide_player_name,
    combine_fide_player_names,
    validate_date_format
)

@dataclass
class CaseParseFidePlayer:
    player_id: Optional[FidePlayerID]
    exp_id: int


@pytest.mark.parametrize(
    'test_case', [
        CaseParseFidePlayer(
            player_id=FidePlayerID(entity_id='12222'), exp_id=12222
        ),
        CaseParseFidePlayer(
            player_id=FidePlayerID(entity_id=12222), exp_id=12222
        ),
        CaseParseFidePlayer(
            player_id=FidePlayerID(entity_id=10006), exp_id=10006
        )
    ]
)
def test_parse_fide_player(test_case: CaseParseFidePlayer) -> None:
    """Testing the 'parse_fide_player' utility function."""
    assert (
        parse_fide_player(fide_player=test_case.player_id) == test_case.exp_id
    )


@pytest.mark.parametrize(
    'test_case', [
        CaseParseFidePlayer(
            player_id=FidePlayerID(entity_id='55332'), exp_id=55332
        ),
        CaseParseFidePlayer(
            player_id=FidePlayerID(entity_id=78332), exp_id=78332
        ),
        CaseParseFidePlayer(player_id=None, exp_id=None)
    ]
)
def test_parse_fide_player_optional(test_case: CaseParseFidePlayer) -> None:
    """Testing the 'parse_fide_player_optional' utility function."""
    assert (
        parse_fide_player_optional(fide_player=test_case.player_id) == test_case.exp_id
    )


@dataclass
class CaseBuildURL:
    base_url: str
    segments: Union[str, int]
    exp_url: str


@pytest.mark.parametrize(
    'test_case', [
        CaseBuildURL(
            base_url='https://fide.com/calendar/',
            segments='53932',
            exp_url='https://fide.com/calendar/53932'
        ),
        CaseBuildURL(
            base_url='https://fide.com/calendar/',
            segments=53932, 
            exp_url='https://fide.com/calendar/53932'
        ),
        CaseBuildURL(
            base_url='https://fide.com/calendar/',
            segments='54198', 
            exp_url='https://fide.com/calendar/54198'
        )
    ]
)
def test_build_url(test_case: CaseBuildURL) -> None:
    """Testing the 'build_url' utility function."""
    assert (
        build_url(base=test_case.base_url, segments=test_case.segments) == test_case.exp_url
    )


@dataclass
class CaseCleanFidePlayerName:
    name: str
    exp_first_name: str
    exp_last_name: str


@pytest.mark.parametrize(
    'test_case', [
        CaseCleanFidePlayerName(
            name='Carlsen, Magnus', exp_first_name='Magnus', exp_last_name='Carlsen'
        ),
        CaseCleanFidePlayerName(
            name='Magnus Carlsen', exp_first_name='Magnus Carlsen', exp_last_name=None
        ),
        CaseCleanFidePlayerName(
            name='Carlsen, Magnus The Goat', exp_first_name='Magnus The Goat', exp_last_name='Carlsen'
        )
    ]
)
def test_clean_fide_player_name(test_case: CaseCleanFidePlayerName) -> None:
    """Testing the 'clean_fide_player_name' utility function."""
    assert clean_fide_player_name(name=test_case.name) == (
        test_case.exp_first_name, test_case.exp_last_name
    )


@dataclass
class CaseCombineFidePlayerName:
    first_name: str
    last_name: str
    exp_name: str


@pytest.mark.parametrize(
    'test_case', [
        CaseCombineFidePlayerName(
            first_name='Magnus', last_name='Carlsen', exp_name='Carlsen, Magnus'
        ),
        CaseCombineFidePlayerName(
            first_name='Hikaru', last_name='Nakamura', exp_name='Nakamura, Hikaru'
        ),
        CaseCombineFidePlayerName(
            first_name='', last_name='Carlsen', exp_name='Carlsen, '
        )
    ]
)
def test_combine_fide_player_name(test_case: CaseCombineFidePlayerName) -> None:
    """Testing the 'combine_fide_player_name' utility function."""
    assert combine_fide_player_names(
        first_name=test_case.first_name, last_name=test_case.last_name
    ) == test_case.exp_name


@dataclass
class CaseValidateDateFormat:
    date: str
    date_format: str
    exp_date: str


@pytest.mark.parametrize(
    'test_case', [
        CaseValidateDateFormat(
            date='2024-04-01 12:03:00', date_format='%Y-%m-%d %H:%M:%S', exp_date='2024-04-01'
        ),
        CaseValidateDateFormat(date='1987', date_format='%Y', exp_date='1987-01-01'),
        CaseValidateDateFormat(date='2024-Feb', date_format='%Y-%b', exp_date='2024-02-01')
    ]
)
def test_validate_date_format(test_case: CaseValidateDateFormat) -> None:
    """Testing the 'validate_date_format' utility function."""
    assert validate_date_format(
        date=test_case.date, date_format=test_case.date_format
    ) == test_case.exp_date


@dataclass
class CaseFromPlayerModel:
    player: Dict[str, Any]
    exp_first_name: str
    exp_last_name: str
    exp_model_dump: str


@pytest.mark.parametrize(
    'test_case', [
        CaseFromPlayerModel(
            player={
                'id': '1503014',
                'name': 'Carlsen, Magnus',
                'title': 'GM',
                'country': 'NOR',
            },
            exp_first_name='Magnus',
            exp_last_name='Carlsen',
            exp_model_dump={
                'name': 'Magnus Carlsen',
                'player_id': 1503014,
                'title': 'GM',
                'country': 'NOR',
            }
        )
    ]
)
def test_from_player_model(test_case: CaseFromPlayerModel) -> None:
    """Testing the 'from_player_model' utility function."""
    first_name, last_name, model_dump = from_player_model(
        player=test_case.player, fide_player_model=FidePlayerRaw
    )
    assert test_case.exp_first_name == first_name
    assert test_case.exp_last_name == last_name
    assert test_case.exp_model_dump == model_dump