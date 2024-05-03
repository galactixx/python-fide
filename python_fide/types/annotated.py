from typing_extensions import Annotated
from typing import Optional, Union
from datetime import datetime, date

from pydantic import BaseModel
from pydantic.functional_validators import BeforeValidator

from python_fide.utils.general import validate_date_format

class Date(BaseModel):
    """
    """
    date_iso: Optional[str]
    date_original: str
    date_original_format: str

    @property
    def as_date(self) -> Optional[date]:
        datetime_as_date = self.as_datetime
        return datetime_as_date.date() if datetime_as_date is not None else None 

    @property
    def as_datetime(self) -> Optional[datetime]:
        return datetime.strptime(self.date_iso, '%Y-%m-%d') if self.date_iso is not None else None
    
    @classmethod
    def from_date_format(cls, date: str, date_format: str) -> 'Date':
        date_iso = validate_date_format(date=date, date_format=date_format)
        return cls(
            date_iso=date_iso, date_original=date, date_original_format=date_format
        )


def _isinstance_date(func):
    def inner(date: Union[str, dict, Date]) -> Date:
        if isinstance(date, str):
            return func(date=date)
        elif isinstance(date, dict):
            return Date(**date)
        elif isinstance(date, Date):
            return date
        else:
            raise TypeError(
                f"{type(date)} not a valid type, expecting a str or dict"
            )
    return inner


@_isinstance_date
def validate_date_year_month(date: Union[str, dict]) -> Date:
    return Date.from_date_format(date=date, date_format='%Y-%b')


@_isinstance_date
def validate_date_iso(date: Union[str, dict]) -> Date:
    return Date.from_date_format(date=date, date_format='%Y-%m-%d')


@_isinstance_date
def validate_date_year(date: Union[str, dict]) -> Date:
    return Date.from_date_format(date=date, date_format='%Y')


@_isinstance_date
def validate_datetime(date: Union[str, dict]) -> Date:
    return Date.from_date_format(date=date, date_format='%Y-%m-%d %H:%M:%S')


DateISO = Annotated[Date, BeforeValidator(validate_date_iso)]
DateYear = Annotated[Date, BeforeValidator(validate_date_year)]
DateTime = Annotated[Date, BeforeValidator(validate_datetime)]
DateYearMonth = Annotated[Date, BeforeValidator(validate_date_year_month)]