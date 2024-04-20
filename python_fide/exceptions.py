class BaseError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message
    

class InvalidFideIDError(BaseError):
    def __init__(self, message: str):
        super().__init__(message=message)
        

class InvalidFormatError(BaseError):
    def __init__(self):
        super().__init__(
            message=(
                "The data parser encountered an error. Please ensure the data adheres to the expected schema."
            )
        )