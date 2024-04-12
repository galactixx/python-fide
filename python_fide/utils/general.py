import sys
from typing import Optional, Tuple

from urllib.parse import urljoin

def clean_fide_player_name(name: str) -> Tuple[str, str]:
    player_first_name = ' '.join(
        name.strip() for name in name.split(',')[1:]
    )
    player_last_name = name.split(',')[0].strip()
    return player_first_name, player_last_name


def create_url(base: str, segments: str) -> str:
    if not base.endswith('/'):
        base += '/'

    return urljoin(base=base, url=segments)


def validate_limit(limit: Optional[int]) -> int:
    if limit is None:
        return sys.maxsize
    else:
        assert isinstance(limit, int)
        assert limit > 0
        return limit