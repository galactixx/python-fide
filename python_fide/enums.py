from enum import Enum

class Period(Enum):
    """The periods in which to filter the historical ratings."""
    ONE_YEAR = 1
    TWO_YEARS = 2
    THREE_YEARS = 3
    FIVE_YEARS = 5
    ALL_YEARS = 0


class RatingCategory(Enum):
    """The categories in which to filter the top ten rankings."""
    OPEN = 'open'
    JUNIORS = 'juniors'
    GIRLS = 'girls'
    WOMEN = 'women'