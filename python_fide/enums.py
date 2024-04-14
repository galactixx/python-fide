from enum import Enum

class Period(Enum):
    ONE_YEAR = 1
    TWO_YEARS = 2
    THREE_YEARS = 3
    FIVE_YEARS = 5
    ALL_YEARS = 0


class RatingCategory(Enum):
    OPEN = 'open'
    JUNIORS = 'juniors'
    GIRLS = 'girls'
    WOMEN = 'women'