from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

import dacite

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value
from pyvultr.v2.base import BaseVultrV2


@dataclass
class BlockStorageItem(BaseDataclass):
    id: str
    cost: float
    status: str
    size_gb: int
    region: str
    attached_to_instance: str
    date_created: str
    label: str
    mount_id: str


class BlockStorage(BaseVultrV2):
    """Vultr BlockStorage API.

    Block Storage volumes are highly-available, redundant, SSD backed, and expandable from 10 GB to 10,000 GB.
    Block storage volumes can be formatted with your choice of filesystems and moved between server instances as needed.

    Attributes:
        api_key: Vultr API key, we get it from env variable `VULTR_API_TOKEN` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "blocks")

    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[BlockStorageItem]:
        """List all Block Storage in your account.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: the capacity of the VultrPagination[BlockStorageItem],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[BlockStorageItem]: a paginated list of `BlockStorageItem`.
        """
        return VultrPagination[BlockStorageItem](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=BlockStorageItem,
            capacity=capacity,
        )

    def create(self, region: str, size_gb: int, label: str = None) -> BlockStorageItem:
        """Create new Block Storage in a `region` with a size of `size_gb`. Size may range between 10 and 10000.

        Args:
            region: The Region id where the Block Storage will be created.
            size_gb: Size in GB may range between 10 and 10000.
            label: The user-supplied label.

        Returns:
            BlockStorageItem: A `BlockStorageItem` object.
        """
        _json = {
            "region": region,
            "size_gb": size_gb,
            "label": label,
        }
        resp = self._post(json=_json)
        return dacite.from_dict(data_class=BlockStorageItem, data=get_only_value(resp))

    def get(self, block_id: str) -> BlockStorageItem:
        """Get information for Block Storage.

        Args:
            block_id: The Block Storage id.

        Returns:
            BlockStorageItem: A `BlockStorageItem` object.
        """
        resp = self._get(f"/{block_id}")
        return dacite.from_dict(data_class=BlockStorageItem, data=get_only_value(resp))

    def update(self, block_id: str, size_gb: int = None, label: str = None):
        """Update information for Block Storage.

        Args:
            block_id: The Block Storage id.
            size_gb: New size of the Block Storage in GB. Size may range between 10 and 10000.
            label: The user-supplied label.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "size_gb": size_gb,
            "label": label,
        }
        return self._patch(f"/{block_id}", json=_json)

    def attach(self, block_id: str, instance_id: str, live: bool = None):
        """Attach Block Storage to Instance `instance_id`.

        Args:
            block_id: The Block Storage id.
            instance_id: Attach the Block Storage to this Instance id.
            live: Attach Block Storage without restarting the Instance.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "instance_id": instance_id,
            "live": live,
        }
        return self._post(f"/{block_id}/attach", json=_json)

    def detach(self, block_id: str, live: bool = None):
        """Detach Block Storage.

        Args:
            block_id: The Block Storage id.
            live: Detach Block Storage without restarting the Instance.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "live": live,
        }
        return self._post(f"/{block_id}/detach", json=_json)

    def delete(self, block_id: str):
        """Delete Block Storage.

        Args:
            block_id: THe Block Storage id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{block_id}")
