class BaseError(Exception):
    """Base error class."""
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message
    

class InvalidFideIDError(BaseError):
    """Error indicating that the Fide ID passed is invalid."""
    def __init__(self, message: str):
        super().__init__(message=message)
        

class InvalidFormatError(BaseError):
    """Error indicating that the format of the response is not what is expected."""
    def __init__(self):
        super().__init__(
            message=(
                "The data parser encountered an error. Please ensure the data adheres to the expected schema."
            )
        )