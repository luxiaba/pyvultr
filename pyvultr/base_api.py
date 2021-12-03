import logging
import os
from abc import ABC, abstractmethod
from enum import Enum, unique
from typing import Any, Dict, Optional
from urllib.parse import SplitResult, urlsplit

import requests
from requests import Response

from pyvultr.exception import NoAPIKeyException
from pyvultr.utils.box import remove_none

log = logging.getLogger(__name__)
DEFAULT_TIMEOUT = 10.00
ENV_TOKEN_NAME = "VULTR_API_KEY"  # nosec: false B105(hardcoded_password_string) by bandit
_session = requests.Session()


@unique
class SupportHttpMethod(Enum):
    """See [HTTP Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)."""

    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    ...


class BaseAPI(ABC):
    def _request(self, method: SupportHttpMethod, endpoint: Optional[str], **kwargs) -> Any:
        _url = self._get_url(endpoint)

        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        self.before_request(method=method, url=_url, kwargs=kwargs)

        resp = _session.request(method=method.value, url=_url, **kwargs)

        if not resp.ok:
            log.error(f"Request to {self.__class__.__name__}: {_url}, failed: {resp.text}")
        return self.after_response(resp)

    @property
    @abstractmethod
    def base_url(self) -> str:
        """Get base url for all API in this section."""
        ...

    def _get_url(self, endpoint: str = None) -> str:
        if not endpoint:
            return self.base_url
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    @property
    def url_meta(self, endpoint=None) -> SplitResult:
        """Get url meta information."""
        return urlsplit(self._get_url(endpoint))

    def before_request(self, method: SupportHttpMethod, url: Optional[str], kwargs: Dict):
        """Unified preprocessing before request."""
        ...

    # noinspection PyMethodMayBeStatic
    def after_response(self, response: Response) -> Any:
        """Unified preprocessing after response."""
        return response

    def _get(self, endpoint: Optional[str] = None, params=None, **kwargs):
        _params = remove_none(params) or None
        return self._request(SupportHttpMethod.GET, endpoint, params=_params, **kwargs)

    def _head(self, endpoint: Optional[str] = None, **kwargs):
        return self._request(SupportHttpMethod.HEAD, endpoint, **kwargs)

    def _post(self, endpoint: Optional[str] = None, data=None, json=None, **kwargs):
        _json = remove_none(json) or None
        return self._request(SupportHttpMethod.POST, endpoint, data=data, json=_json, **kwargs)

    def _put(self, endpoint: Optional[str] = None, data=None, json=None, **kwargs):
        _json = remove_none(json) or None
        return self._request(SupportHttpMethod.PUT, endpoint, data=data, json=_json, **kwargs)

    def _delete(self, endpoint: Optional[str] = None, **kwargs):
        return self._request(SupportHttpMethod.DELETE, endpoint, **kwargs)

    def _options(self, endpoint: Optional[str] = None, **kwargs):
        return self._request(SupportHttpMethod.OPTIONS, endpoint, **kwargs)

    def _patch(self, endpoint: Optional[str] = None, data=None, json=None, **kwargs):
        _json = remove_none(json) or None
        return self._request(SupportHttpMethod.PATCH, endpoint, data=data, json=_json, **kwargs)


@unique
class SupportVultrAPIVersion(Enum):
    V1 = "v1"
    V2 = "v2"


class BaseVultrAPI(BaseAPI):
    def __init__(self, version: SupportVultrAPIVersion, api_key: str = None):
        self.api_version: SupportVultrAPIVersion = version
        self.__token: str = os.getenv(ENV_TOKEN_NAME) or api_key
        if not self.__token:
            raise NoAPIKeyException(f"Missing Vultr API Key: no `{ENV_TOKEN_NAME}` env or `api_key` arg.")

    @property
    def base_url(self) -> str:
        """Get base url for all API in this section."""
        return f"https://api.vultr.com/{self.api_version.value}/"

    def before_request(self, method: SupportHttpMethod, url: Optional[str], kwargs: Dict):
        """Unified preprocessing before request."""
        headers = kwargs.setdefault("headers", {})
        headers["Authorization"] = f"Bearer {self.__token}"
        log.debug(f"Vultr API({self.api_version}) request: method: {method.value}, url: {url}, args: {kwargs}")
