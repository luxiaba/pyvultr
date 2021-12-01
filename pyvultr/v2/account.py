from dataclasses import dataclass
from typing import List, Optional

from pyvultr.utils import BaseDataclass, get_only_value

from .base import BaseVultrV2


@dataclass
class AccountInfo(BaseDataclass):
    name: str
    email: str
    acls: List[str]
    balance: float
    pending_charges: float
    last_payment_date: str
    last_payment_amount: float


class Account(BaseVultrV2):
    """Vultr Account API.

    Reference: https://www.vultr.com/zh/api/#tag/account

    Read-only information about your user account and billing information.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$ENV_TOKEN_NAME` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    def get(self) -> AccountInfo:
        """Get your Vultr account, permission, and billing information.

        Returns:
            AccountInfo: A `AccountInfo` object.
        """
        resp = self._get("/account")
        return AccountInfo.from_dict(get_only_value(resp))
