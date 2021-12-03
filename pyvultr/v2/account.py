from dataclasses import dataclass
from typing import List, Optional

from pyvultr.utils import BaseDataclass, get_only_value

from .base import BaseVultrV2, command


@dataclass
class AccountInfo(BaseDataclass):
    name: str  # Your username.
    email: str  # Your email.
    acls: List[str]  # An array of permission granted, see `enums.ACL` for details.
    balance: float  # Your current account balance.
    pending_charges: float  # Un-billed charges for this month.
    last_payment_date: str  # Date of your last payment.
    last_payment_amount: float  # The amount of your last payment.


class AccountAPI(BaseVultrV2):
    """Vultr Account API.

    Reference: https://www.vultr.com/api/#tag/account

    Read-only information about your user account and billing information.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @command
    def get(self) -> AccountInfo:
        """Get your Vultr account, permission, and billing information.

        Returns:
            AccountInfo: A `AccountInfo` object.
        """
        resp = self._get("/account")
        return AccountInfo.from_dict(get_only_value(resp))
