from enum import Enum


class RatingPeriod(Enum):
    """The periods in which to filter the historical ratings."""

    ONE_YEAR = 1
    TWO_YEARS = 2
    THREE_YEARS = 3
    FIVE_YEARS = 5
    ALL_YEARS = 0
