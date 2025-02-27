class BaseError(Exception):
    """Base error class."""

    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class InvalidFideIDError(BaseError):
    """Error indicating that the Fide ID passed is invalid."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message)


class InvalidFormatError(BaseError):
    """
    Error indicating that the format of the response is
    not what is expected.
    """

    def __init__(self) -> None:
        super().__init__(
            message=("Please ensure the data adheres to the expected schema.")
        )
