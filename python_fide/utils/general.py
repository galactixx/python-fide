from datetime import datetime
from typing import Optional, Tuple, Union
from urllib.parse import urljoin


def validate_date_format(date: str, date_format: str) -> Optional[str]:
    """
    Validation of a specific date format given a string date. Will
    return an ISO formatted date (%Y-%m-%d). If the date does not
    match the format provided, then None is returned instead of the
    formatted date.

    Args:
        date (str): A date represented as a string in some format.
        date_format (str): A string format of the date.

    Returns:
        str | None: A string ISO formatted date or None if the date
            string did not match the format provided.
    """
    try:
        month_reformatted = datetime.strptime(date, date_format)
        month_date = datetime.strftime(month_reformatted, "%Y-%m-%d")
    except ValueError:
        month_date = None
    finally:
        return month_date


def clean_fide_player_name(name: str) -> Tuple[str, Optional[str]]:
    """
    Cleans the raw player name field from the API response.

    If there is a comma in the name, it is clear that the last
    name is separated from the rest of the name. Thus, we treat
    anything before the comma as the last name and anything
    after is combined into the first name.

    If there is no comma found in the name, then the entire name
    is treated as the first name, and the last name is returned
    as None.

    Args:
        name (str): The full name of the player returned from
            the raw API response.

    Returns:
        Tuple[str, str | None]: A tuple of a string first name
            and a string last name. The last name can be None if
            it was not detected reliably.
    """
    if "," not in name:
        return name, None
    else:
        name_split = name.split(",")
        last_name = name_split[0].strip()
        first_name = " ".join(name.strip() for name in name_split[1:])
        return first_name, last_name


def build_url(base: str, segments: Union[int, str]) -> str:
    """
    Builds a URL based on a base URL and segments.

    Args:
        base (str): A string base URL.
        segments (int | str): A string or integer URL segment.

    Returns:
        str: A complete URL consolidating the base and segments.
    """
    if isinstance(segments, int):
        segments = str(segments)

    if not base.endswith("/"):
        base += "/"

    return urljoin(base=base, url=segments)
