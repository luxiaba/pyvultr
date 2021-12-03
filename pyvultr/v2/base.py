import functools
import logging
import time
import types
from collections import defaultdict
from dataclasses import asdict, is_dataclass
from typing import Any, Callable, Dict, Iterable, List, Optional

from requests import Response

from pyvultr.base_api import BaseVultrAPI, SupportHttpMethod, SupportVultrAPIVersion
from pyvultr.exception import APIException
from pyvultr.utils import BaseDataclass, VultrPagination
from pyvultr.utils.box import make_colorful

log = logging.getLogger(__name__)

# Collect a list of services that each API can provide to the outside world.
# eg: {
#     'AccountAPI': ['get'],
#     'InstanceAPI': ['create', 'delete', 'list', ...],
#     ...
# }
COMMANDS: Dict[str, List[str]] = defaultdict(list)

# Last time you requested Vultr API.
LATEST_REQ_AT = time.time()
# Due to the frequency limitation of Vultr.
# We limit the min access interval to prevent 429(Too many requests) or other similar errors.
MIN_REQ_INTERVAL_SEC = 0.1


class CommandWrapper:
    def __init__(self):
        self.is_cli: bool = False

    @staticmethod
    def make_beautiful(obj: Any):
        """Make the object colorful to show."""
        if isinstance(obj, BaseDataclass):
            return make_colorful(obj.to_dict())
        elif isinstance(obj, VultrPagination):
            # TODO limit one page or not.
            return "".join(make_colorful(i) for i in obj)
        elif is_dataclass(obj):
            return make_colorful(asdict(obj))
        elif isinstance(obj, (dict, list, tuple)):
            return make_colorful(obj)
        elif isinstance(obj, (set, types.GeneratorType)):
            return make_colorful([i for i in obj])
        return str(obj)


command_wrapper = CommandWrapper()


def command(func: Callable):
    """Decorate function to register a command.

    1. Collect all commands that each API can provide to the outside world to `COMMANDS`.
    2. Another function is to unified processing of output, eg: make beautiful output in CLI
    """
    qualname: str = func.__qualname__
    try:
        *_, cls_name, func_name = qualname.rsplit(".", 2)
        COMMANDS[cls_name].append(func_name)
    except (AttributeError, ValueError):
        log.error(f"Can't get class name and func name from {func}, qualname: {qualname}")

    @functools.wraps(func)
    def decorator(*func_args, **func_kwargs):
        func_returned = func(*func_args, **func_kwargs)
        if not command_wrapper.is_cli:
            return func_returned
        return command_wrapper.make_beautiful(func_returned)

    return decorator


class BaseVultrV2(BaseVultrAPI):
    """Vultr Base V2 API.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: str = None):
        super().__init__(SupportVultrAPIVersion.V2, api_key)

    def __dir__(self) -> Iterable[str]:
        """Return all available commands in each API."""
        return COMMANDS.get(self.__class__.__name__)

    def before_request(self, method: SupportHttpMethod, url: Optional[str], kwargs: Dict):
        """Unified preprocessing before request.

        Args:
            method: SupportHttpMethod.
            url: request url.
            kwargs: request kwargs.
        """
        self.frequency_detector()
        super().before_request(method, url, kwargs)

    def after_response(self, resp: Response) -> Dict:
        """For unified pretreatment of response data.

        Args:
            resp: requests.Response object.

        Returns:
            Dict: response json data.
        """
        code, text = resp.status_code, resp.text
        log.debug(f"Vultr API({self.api_version}) response: code: {code}, content: {text}")

        if not resp.ok:
            log.error(f"Error in calling Vultr API: code : {code}, response: {text}")
            raise APIException(resp)

        return resp.json() if resp.text else None

    @staticmethod
    def frequency_detector():
        """Frequency Detector.

        Vultr API has a call frequency limit, which cannot exceed 20/s.
        Here, a simple current limiter is implemented.
        """
        global MIN_REQ_INTERVAL_SEC, LATEST_REQ_AT
        req_at = time.time()
        if req_at - LATEST_REQ_AT <= MIN_REQ_INTERVAL_SEC:
            time.sleep(MIN_REQ_INTERVAL_SEC)
        LATEST_REQ_AT = req_at
