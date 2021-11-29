import logging
import time
from typing import Dict, Optional

from requests import Response

from pyvultr.base_api import BaseVultrAPI, SupportHttpMethod, SupportVultrAPIVersion
from pyvultr.exception import APIException

log = logging.getLogger(__name__)
MIN_INTERVAL_SEC = 0.1
LATEST_ACCESS_AT = time.time()


class BaseVultrV2(BaseVultrAPI):
    """Vultr Base V2 API.

    Attributes:
        api_key: Vultr API key, we get it from env variable `VULTR_API_TOKEN` if not provided.
    """

    def __init__(self, api_key: str = None):
        super().__init__(SupportVultrAPIVersion.V2, api_key)

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
        log.debug(f"Vultr API({self.version}) response: code: {code}, content: {text}")

        if not resp.ok:
            log.error(f"Error in calling Vultr API: code : {code}, resp: {text}")
            raise APIException(code, text)

        return resp.json()

    @staticmethod
    def frequency_detector():
        """Frequency Detector.

        Vultr API has a call frequency limit, which cannot exceed 20/s.
        Here, a simple current limiter is implemented.
        """
        global MIN_INTERVAL_SEC, LATEST_ACCESS_AT
        access_at = time.time()
        if access_at - LATEST_ACCESS_AT <= MIN_INTERVAL_SEC:
            time.sleep(MIN_INTERVAL_SEC)
        LATEST_ACCESS_AT = access_at
