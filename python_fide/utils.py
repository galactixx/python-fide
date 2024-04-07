import sys
from typing import Optional

from urllib.parse import urljoin

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