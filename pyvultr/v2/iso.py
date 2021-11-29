from dataclasses import dataclass
from functools import partial
from typing import Optional

import dacite

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value
from pyvultr.v2.base import BaseVultrV2


@dataclass
class ISOItem(BaseDataclass):
    id: str
    date_created: str
    filename: str
    size: int
    md5sum: str
    sha512sum: str
    status: str


@dataclass
class PublicISOItem(BaseDataclass):
    id: str
    name: str
    description: str
    md5sum: str


class ISO(BaseVultrV2):
    """Vultr ISO API.

    Upload and boot instances from your ISO, or choose one from our public ISO library. See our ISO documentation.

    Attributes:
        api_key: Vultr API key, we get it from env variable `VULTR_API_TOKEN` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[ISOItem]:
        """Get the ISOs in your account.

        Args:
            per_page: number of items requested per page. Default is 100 and Max is 500.
            cursor: cursor for paging.
            capacity: the capacity of the VultrPagination[ISOItem],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[ISOItem]: A paginated list of `ISOItem`.
        """
        fetcher = partial(self._get, endpoint="/iso")
        return VultrPagination[ISOItem](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=ISOItem,
            capacity=capacity,
        )

    def create(self, url: str) -> ISOItem:
        """Create a new ISO in your account from `url`.

        Args:
            url: Public URL location of the ISO image to download. Example: `https://example.com/my-iso.iso`.

        Returns:
            ISOItem: An ISOItem object.
        """
        _json = {
            "url": url,
        }
        resp = self._post(json=_json)
        return dacite.from_dict(data_class=ISOItem, data=get_only_value(resp))

    def get(self, iso_id: str) -> ISOItem:
        """Get information for an ISO.

        Args:
            iso_id: The ISO id.

        Returns:
            ISOItem: An ISOItem object.
        """
        resp = self._get(f"/iso/{iso_id}")
        return dacite.from_dict(data_class=ISOItem, data=get_only_value(resp))

    def delete(self, iso_id: str):
        """Delete an ISO.

        Args:
            iso_id: The ISO id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/iso/{iso_id}")

    def list_public(
        self,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[PublicISOItem]:
        """Get the ISOs in your account.

        Args:
            per_page: number of items requested per page. Default is 100 and Max is 500.
            cursor: cursor for paging.
            capacity: the capacity of the VultrPagination[PublicISOItem],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[PublicISOItem]: a paginated list of `PublicISOItem`.
        """
        fetcher = partial(self._get, endpoint="/iso-public")
        return VultrPagination[PublicISOItem](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=PublicISOItem,
            capacity=capacity,
        )
