from datetime import datetime
from typing import Optional, Union
from urllib.parse import urljoin


def validate_date_format(date: str, date_format: str) -> Optional[str]:
    """
    Validation of a specific date format given a string date. Will
    return an ISO formatted date (%Y-%m-%d). If the date does not
    match the format provided, then None is returned instead of the
    formatted date.
    """
    try:
        month_reformatted = datetime.strptime(date, date_format)
        month_date = datetime.strftime(month_reformatted, "%Y-%m-%d")
    except ValueError:
        month_date = None
    finally:
        return month_date


def build_url(base: str, segments: Union[int, str]) -> str:
    """Builds a URL based on a base URL and segments."""
    if isinstance(segments, int):
        segments = str(segments)

    if not base.endswith("/"):
        base += "/"

    return urljoin(base=base, url=segments)
