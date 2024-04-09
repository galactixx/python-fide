class BaseError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message
    

class NoResultsError(BaseError):
    def __init__(self):
        super().__init__(
            message='there are no results associated with query'
        )


class IncorrectAttrError(BaseError):
    def __init__(self):
        super().__init__(
            message='attribute was not found due to incorrect or outdated mapping'
        )