from typing_extensions import Annotated

from pydantic.functional_validators import AfterValidator

from python_fide.utils.general import validate_date_format

def validate_date_year_month(date: str) -> str:
    """"""
    return validate_date_format(date=date, date_format='%Y-%b')


def validate_date_iso(date: str) -> str:
    """"""
    return validate_date_format(date=date, date_format='%Y-%m-%d')


def validate_date_year(year: str) -> str:
    """"""
    return validate_date_format(date=year, date_format='%Y')


def validate_datetime(date: str) -> str:
    """"""
    return validate_date_format(date=date, date_format='%Y-%m-%d %H:%M:%S')


DateISO = Annotated[str, AfterValidator(validate_date_iso)]
DateYear = Annotated[str, AfterValidator(validate_date_year)]
DateTime = Annotated[str, AfterValidator(validate_datetime)]
DateYearMonth = Annotated[str, AfterValidator(validate_date_year_month)]