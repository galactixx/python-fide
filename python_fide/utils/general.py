import sys
from typing import List, Optional, Tuple, Union
import re
from datetime import datetime

from urllib.parse import urljoin

def validate_date_format(date: str, date_format: str) -> Optional[str]:
    """
    """
    try:
        month_reformatted = datetime.strptime(date, date_format)
        month_date = datetime.strftime(month_reformatted, '%Y-%m-%d')
    except ValueError:
        month_date = None
    finally:
        return month_date


def remove_non_digits_from_string(text: str) -> str:
    """
    """
    return re.sub(r"[^\d]", "", text)


def join_strings_by_space(strings: List[str]) -> str:
    """
    """
    return ' '.join(
        name.strip() for name in strings
    )


def combine_fide_player_names(first_name: str, last_name: str) -> str:
    return f'{last_name}, {first_name}'


def parse_fide_player_name(name: str, split_char: str) -> Tuple[str, Optional[str]]:
    """
    """
    name_split = name.split(split_char)
    if len(name_split) == 1:
        player_first_name = name_split[0].strip()
        return player_first_name, None
    else:
        player_last_name = name_split[0].strip()
        player_first_name = join_strings_by_space(strings=name_split[1:])
        return (
            player_first_name, player_last_name
        )


def clean_fide_player_name(name: str) -> Tuple[str, str]:
    """
    """
    if ',' not in name:
        first_name, last_name = parse_fide_player_name(
            name=name, split_char=' '
        )
    else:
        first_name, last_name = parse_fide_player_name(
            name=name, split_char=','
        )
    return first_name, last_name


def build_url(base: str, segments: Union[int, str]) -> str:
    """
    """
    if isinstance(segments, int):
        segments = str(segments)

    if not base.endswith('/'):
        base += '/'

    return urljoin(base=base, url=segments)


def validate_limit(limit: Optional[int]) -> int:
    """
    """
    if limit is None:
        return sys.maxsize
    else:
        assert isinstance(limit, int)
        assert limit > 0
        return limit