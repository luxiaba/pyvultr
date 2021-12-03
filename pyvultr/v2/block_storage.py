from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value

from .base import BaseVultrV2, command


@dataclass
class BlockStorage(BaseDataclass):
    id: str  # A unique ID for the Block Storage.
    cost: float  # The monthly cost of this Block Storage.
    status: str  # The current status of this Block Storage, see `enums.BlockStorageStatus` for details.
    size_gb: int  # Size of the Block Storage in GB.
    # The Region id where the block is located, check `RegionAPI.list` and `RegionItem.id` for available regions.
    region: str
    # The Instance id with this Block Storage attached, check `InstanceItem.id` for available instances.
    attached_to_instance: str
    date_created: str  # The date this Block Storage was created.
    label: str  # The user-supplied label.
    # An ID associated with the instance, when mounted the ID can be found in /dev/disk/by-id prefixed with virtio.
    mount_id: str


class BlockStorageAPI(BaseVultrV2):
    """Vultr BlockStorage API.

    Reference: https://www.vultr.com/api/#tag/block

    Block Storage volumes are highly-available, redundant, SSD backed, and expandable from 10 GB to 10,000 GB.
    Block storage volumes can be formatted with your choice of filesystems and moved between server instances as needed.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "blocks")

    @command
    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[BlockStorage]:
        """List all Block Storage in your account.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: The capacity of the VultrPagination[BlockStorageItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[BlockStorage]: A list-like object of `BlockStorageItem` object.
        """
        return VultrPagination[BlockStorage](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=BlockStorage,
            capacity=capacity,
        )

    @command
    def create(self, region: str, size_gb: int, label: str = None) -> BlockStorage:
        """Create new Block Storage in a `region` with a size of `size_gb`. Size may range between 10 and 10000.

        Args:
            region: The Region id where the Block Storage will be created.
            size_gb: Size in GB may range between 10 and 10000.
            label: The user-supplied label.

        Returns:
            BlockStorage: A `BlockStorageItem` object.
        """
        _json = {
            "region": region,
            "size_gb": size_gb,
            "label": label,
        }
        resp = self._post(json=_json)
        return BlockStorage.from_dict(get_only_value(resp))

    @command
    def get(self, block_id: str) -> BlockStorage:
        """Get information for Block Storage.

        Args:
            block_id: The Block Storage id.

        Returns:
            BlockStorage: A `BlockStorageItem` object.
        """
        resp = self._get(f"/{block_id}")
        return BlockStorage.from_dict(get_only_value(resp))

    @command
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

    @command
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

    @command
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

    @command
    def delete(self, block_id: str):
        """Delete Block Storage.

        Args:
            block_id: THe Block Storage id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{block_id}")
