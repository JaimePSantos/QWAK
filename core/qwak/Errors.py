class Error(BaseException):
    def __init__(self, error_name: str, details: str):
        """Initialize the error instance with error name and details

        Parameters
        ----------
        error_name : str
            Name of the error.
        details : str
            Additional details about the error.
        """
        self.error_name = error_name
        self.details = details

    def as_string(self) -> str:
        """Return a string representation of the error message

        Returns
        -------
        str
            String representation of the error message.
        """
        return f"{self.error_name}: {self.details}\n"


class StateOutOfBounds(Error):
    def __init__(self, details: str) -> None:
        """This exception is raised when the state is out of the expected bounds.
        Initialize the error instance with error name and details.

        Parameters
        ----------
        details : str
            Additional details about the error.
        """
        super().__init__("Condition out of bounds: ", details)


class NonUnitaryState(Error):
    def __init__(self, details: str) -> None:
        """This exception is raised when the state is not unitary.
        Initialize the error instance with error name and details.

        Parameters
        ----------
        details : str
            Additional details about the error.
        """
        super().__init__("State is not unitary: ", details)


class UndefinedTimeList(Error):
    def __init__(self, details: str) -> None:
        """This exception is raised when the time interval for multiple walks is undefined.
        Initialize the error instance with error name and details.

        Parameters
        ----------
        details : str
            Additional details about the error.
        """
        super().__init__("Time interval for multiple walks is undefined: ", details)


class EmptyProbDistList(Error):
    def __init__(self, details: str) -> None:
        """This exception is raised when the probability distribution list is empty.
        Initialize the error instance with error name and details.

        Parameters
        ----------
        details : str
            Additional details about the error.
        """
        super().__init__("Probability distribution list is empty: ", details)


class MissingNodeInput(Error):
    def __init__(self, details: str) -> None:
        """This exception is raised when input nodes are required but not provided.
        Initialize the error instance with error name and details.

        Parameters
        ----------
        details : str
            Additional details about the error.
        """
        super().__init__("Input nodes required: ", details)


class MissingGraphInput(Error):
    def __init__(self, details):
        """This exception is raised when a graph is required but not provided.

        Parameters
        ----------
        details : str
            Additional details about the error.
        """
        super().__init__("Graph required: ", details)
