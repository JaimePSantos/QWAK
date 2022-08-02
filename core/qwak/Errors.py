class Error(BaseException):
    """_summary_

    Parameters
    ----------
    BaseException : _type_
        _description_
    """

    def __init__(self, error_name, details):
        """_summary_

        Parameters
        ----------
        error_name : _type_
            _description_
        details : _type_
            _description_
        """
        self.error_name = error_name
        self.details = details

    def as_string(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return f"{self.error_name}: {self.details}\n"


class StateOutOfBounds(Error):
    """_summary_

    Parameters
    ----------
    Error : _type_
        _description_
    """

    def __init__(self, details):
        """_summary_

        Parameters
        ----------
        details : _type_
            _description_
        """
        super().__init__("Condition out of bounds: ", details)


class NonUnitaryState(Error):
    """_summary_

    Parameters
    ----------
    Error : _type_
        _description_
    """

    def __init__(self, details):
        """_summary_

        Parameters
        ----------
        details : _type_
            _description_
        """
        super().__init__("State is not unitary: ", details)


class UndefinedTimeList(Error):
    """_summary_

    Parameters
    ----------
    Error : _type_
        _description_
    """

    def __init__(self, details):
        """_summary_

        Parameters
        ----------
        details : _type_
            _description_
        """
        super().__init__("Time interval for multiple walks is undefined: ", details)

class EmptyProbDistList(Error):
    """_summary_

    Parameters
    ----------
    Error : _type_
        _description_
    """

    def __init__(self, details):
        """_summary_

        Parameters
        ----------
        details : _type_
            _description_
        """
        super().__init__("Probability distribution list is empty: ", details)