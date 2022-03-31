class Error(BaseException):
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def as_string(self):
        return f'{self.error_name}: {self.details}\n'


class StateOutOfBounds(Error):
    def __init__(self, details):
        super().__init__('Condition out of bounds: ', details)
