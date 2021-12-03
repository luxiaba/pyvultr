from dataclasses import dataclass
from functools import partial
from typing import Optional

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value

from .base import BaseVultrV2, command


@dataclass
class ISO(BaseDataclass):
    id: str  # A unique ID for the ISO.
    date_created: str  # Date the ISO was created.
    filename: str  # The ISO filename.
    size: int  # The ISO size in KB.
    md5sum: str  # The calculated md5sum of the ISO.
    sha512sum: str  # The calculated sha512sum of the ISO.
    status: str  # The current status of the ISO, see `enum.ISOStatus` for possible values.


@dataclass
class PublicISOItem(BaseDataclass):
    id: str  # A unique ID for the Vultr Public ISO.
    name: str  # The short name of the Public ISO.
    description: str  # The long description of the Public ISO.
    md5sum: str  # md5sum of the Public ISO.


class ISOAPI(BaseVultrV2):
    """Vultr ISO API.

    Reference: https://www.vultr.com/api/#tag/iso

    Upload and boot instances from your ISO, or choose one from our public ISO library. See our ISO documentation.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @command
    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[ISO]:
        """Get the ISOs in your account.

        Args:
            per_page: number of items requested per page. Default is 100 and Max is 500.
            cursor: cursor for paging.
            capacity: The capacity of the VultrPagination[ISOItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[ISO]: A list-like object of `ISOItem` object.
        """
        fetcher = partial(self._get, endpoint="/iso")
        return VultrPagination[ISO](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=ISO,
            capacity=capacity,
        )

    @command
    def create(self, url: str) -> ISO:
        """Create a new ISO in your account from `url`.

        Args:
            url: Public URL location of the ISO image to download. Example: `https://example.com/my-iso.iso`.

        Returns:
            ISO: An ISOItem object.
        """
        _json = {
            "url": url,
        }
        resp = self._post("/iso", json=_json)
        return ISO.from_dict(get_only_value(resp))

    @command
    def get(self, iso_id: str) -> ISO:
        """Get information for an ISO.

        Args:
            iso_id: The ISO id.

        Returns:
            ISO: An ISOItem object.
        """
        resp = self._get(f"/iso/{iso_id}")
        return ISO.from_dict(get_only_value(resp))

    @command
    def delete(self, iso_id: str):
        """Delete an ISO.

        Args:
            iso_id: The ISO id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/iso/{iso_id}")

    @command
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
            capacity: The capacity of the VultrPagination[PublicISOItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[PublicISOItem]: A list-like object of `PublicISOItem` object.
        """
        fetcher = partial(self._get, endpoint="/iso-public")
        return VultrPagination[PublicISOItem](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=PublicISOItem,
            capacity=capacity,
        )
