from typing import Dict, Optional

from requests import Response


class PYVException(Exception):
    """Base class for all exceptions raised by this module."""

    def __init__(self, *args, **kwargs):
        self.json: Optional[Dict] = None

    def __repr__(self):
        """Return a string representation of the exception."""
        return f"<{self.__class__.__name__} {self.args}>"

    def __str__(self):
        """Return a string representation of the exception."""
        return self.__repr__()


class NoAPIKeyException(PYVException):
    ...


class APIException(PYVException):
    def __init__(self, resp: Response):
        self.__raw_resp = resp
        self.code = resp.status_code
        self.msg = resp.text
        self.try_load_json_content()

    def try_load_json_content(self):
        """Try to load the json content of the response to set error's json content."""
        try:
            self.json = self.__raw_resp.json()
        except (ValueError, TypeError):
            ...

    def __repr__(self):
        """Return a string representation of the exception."""
        return f"<{self.__class__.__name__} {self.code}: {self.msg}>"


class UnexpectedPageDataException(PYVException):
    ...


class NoMorePageDataException(PYVException):
    ...


class OutOfRangePageDataException(PYVException):
    ...
