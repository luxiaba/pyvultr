from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

import dacite

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value
from pyvultr.v2.base import BaseVultrV2


@dataclass
class SnapshotItem(BaseDataclass):
    id: str
    date_created: str
    description: str
    size: int
    status: str
    os_id: int
    app_id: int


class Snapshot(BaseVultrV2):
    """Vultr Snapshot API.

    A snapshot is a point-in-time image of an instance. We do not stop the instance when taking a snapshot.
    Booting from a snapshot is similar to rebooting after a non-graceful restart. Snapshots are physically the
    same as backups, but snapshots are manual while backups run automatically on a schedule.
    See our Snapshot Quickstart Guide for more information.

    Attributes:
        api_key: Vultr API key, we get it from env variable `VULTR_API_TOKEN` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "snapshots")

    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[SnapshotItem]:
        """Get information about all Snapshots in your account.

        Args:
            per_page: number of items requested per page. Default is 100 and Max is 500.
            cursor: cursor for paging.
            capacity: the capacity of the VultrPagination[SnapshotItem],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[SnapshotItem]: A paginated list of `SnapshotItem`.
        """
        return VultrPagination[SnapshotItem](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=SnapshotItem,
            capacity=capacity,
        )

    def create(self, instance_id: str, description: str = None) -> SnapshotItem:
        """Create a new Snapshot for `instance_id`.

        Args:
            instance_id: Create a Snapshot for this `instance_id`.
            description: The user-supplied description of the Snapshot.

        Returns:
            SnapshotItem: The Snapshot object.
        """
        _json = {
            "instance_id": instance_id,
            "description": description,
        }
        resp = self._post(json=_json)
        return dacite.from_dict(data_class=SnapshotItem, data=get_only_value(resp))

    def create_from_url(self, url: str) -> SnapshotItem:
        """Create a new Snapshot from a RAW image located at `url`.

        Args:
            url: The public URL containing a RAW image.

        Returns:
            SnapshotItem: The Snapshot object.
        """
        _json = {
            "url": url,
        }
        resp = self._post("/create-from-url", json=_json)
        return dacite.from_dict(data_class=SnapshotItem, data=get_only_value(resp))

    def get(self, snapshot_id: str) -> SnapshotItem:
        """Get information about a Snapshot.

        Args:
            snapshot_id: The Snapshot ID.

        Returns:
            SnapshotItem: The Snapshot object.
        """
        resp = self._get(f"/{snapshot_id}")
        return dacite.from_dict(data_class=SnapshotItem, data=get_only_value(resp))

    def update(self, snapshot_id: str, description: str):
        """Update the description for a Snapshot.

        Args:
            snapshot_id: The Snapshot ID.
            description: The user-supplied description for the Snapshot.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "description": description,
        }
        return self._put(f"/{snapshot_id}", json=_json)

    def delete(self, snapshot_id: str):
        """Delete a Snapshot.

        Args:
            snapshot_id: The Snapshot ID.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{snapshot_id}")
