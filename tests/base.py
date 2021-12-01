import json
from dataclasses import is_dataclass
from typing import Dict, TypeVar, Union
from unittest import TestCase
from unittest.mock import patch

import dacite

from pyvultr import VultrV2
from pyvultr.base_api import SupportHttpMethod
from pyvultr.utils import get_only_value
from tests.fixture import TestFixture

T = TypeVar("T")
FIXTURES = TestFixture()


class MockResponse:
    def __init__(self, json_body: Dict = None, status_code: int = 200, headers: Dict = None):
        self.status_code = status_code
        self.json_body = json_body
        self.headers = headers or {}

    @property
    def ok(self) -> bool:
        """Return True if the status code less than 400."""
        return self.status_code < 400

    @property
    def text(self) -> str:
        """Return the content of the mock response in str."""
        return self.json_body and json.dumps(self.json_body)

    @property
    def content(self) -> bytes:
        """Return the content of the mock response in bytes."""
        return self.text.encode()

    def json(self) -> Dict:
        """Return the json body of the mock response."""
        return self.json_body


class MockRequest:
    def __init__(
        self,
        method: SupportHttpMethod,
        status_code: int,
        returned: Union[Dict, str] = None,
        headers: Dict = None,
        expected_returned: T = None,
    ):
        self.mock = None
        self._method = method
        self.status_code = status_code
        self.headers = headers
        self.body = returned and self.confirm_body(returned)
        self.expected_returned = expected_returned

    @property
    def method(self):
        """Return the mocked method."""
        return self._method.value

    @staticmethod
    def confirm_body(content) -> Dict:
        """Parse content to return a dict."""
        if isinstance(content, dict):
            return content
        elif isinstance(content, str):
            return FIXTURES.get(content)
        raise TypeError("return_dct must be a dict or a URL from which the JSON could be loaded")

    def __enter__(self):
        """Begins the request mocking."""
        self.patch = patch(
            "pyvultr.base_api.requests.request",
            return_value=MockResponse(json_body=self.body, status_code=self.status_code, headers=self.headers),
        )
        self.mock = self.patch.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Remove the mocked request."""
        self.patch.stop()

    @property
    def url(self):
        """Return the mocked request url."""
        return self.args["url"]

    @property
    def args(self):
        """Return the mocked request arguments."""
        return self.mock.call_args[1]

    @property
    def params(self):
        """Return the mocked request arguments."""
        return self.args.get("params")

    @property
    def req_json(self):
        """Return the mocked request arguments."""
        return self.args.get("json")

    @property
    def python_body(self) -> T:
        """Try convert the mock body content to a python object and return."""
        if is_dataclass(self.expected_returned):
            return dacite.from_dict(self.expected_returned, get_only_value(self.body))
        return self.body


class BaseTest(TestCase):
    def setUp(self):
        """Init the test."""
        self.api_v2 = VultrV2("test_token")

    @staticmethod
    def _get(returned: Union[Dict, str] = None, status_code: int = 200, expected_returned: T = None):
        return MockRequest(SupportHttpMethod.GET, status_code, returned, expected_returned=expected_returned)

    @staticmethod
    def _post(returned: Union[Dict, str] = None, status_code: int = 200, expected_returned: T = None):
        return MockRequest(SupportHttpMethod.POST, status_code, returned, expected_returned=expected_returned)

    @staticmethod
    def _put(returned: Union[Dict, str] = None, status_code: int = 200, expected_returned: T = None):
        return MockRequest(SupportHttpMethod.PUT, status_code, returned, expected_returned=expected_returned)

    @staticmethod
    def _delete(returned: Union[Dict, str] = None, status_code: int = 200, expected_returned: T = None):
        return MockRequest(SupportHttpMethod.DELETE, status_code, returned, expected_returned=expected_returned)

    @staticmethod
    def _options(returned: Union[Dict, str] = None, status_code: int = 200, expected_returned: T = None):
        return MockRequest(SupportHttpMethod.OPTIONS, status_code, returned, expected_returned=expected_returned)

    @staticmethod
    def _patch(returned: Union[Dict, str] = None, status_code: int = 200, expected_returned: T = None):
        return MockRequest(SupportHttpMethod.PATCH, status_code, returned, expected_returned=expected_returned)
