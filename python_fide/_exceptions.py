class BaseError(Exception):
    """Base error class."""

    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class InvalidFideIDError(BaseError):
    """Error indicating that the Fide ID passed is invalid."""

    pass


class InvalidFormatError(BaseError):
    """
    Error indicating that the format of the response is
    not what is expected.
    """

    pass


class InvalidFidePlayerError(BaseError):
    """
    An error indicating that the Fide player ID does not exist.
    """

    pass
