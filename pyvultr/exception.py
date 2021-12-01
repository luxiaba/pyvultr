class PYVException(Exception):
    """Base class for all exceptions raised by this module."""

    ...


class APIException(PYVException):
    def __init__(self, code: int, msg: str = ""):
        self.code = code
        self.msg = msg

    def __repr__(self):
        """Return a string representation of the exception."""
        return f"<APIException code={self.code} msg={self.msg}>"

    def __str__(self):
        """Return a string representation of the exception."""
        return self.__repr__()


class UnexpectedPageDataException(PYVException):
    ...


class NoMorePageDataException(PYVException):
    ...


class OutOfRangePageDataException(PYVException):
    ...
