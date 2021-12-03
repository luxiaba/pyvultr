from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value

from .base import BaseVultrV2, command


@dataclass
class Snapshot(BaseDataclass):
    id: str  # A unique ID for the Snapshot.
    date_created: str  # The date this snapshot was created.
    description: str  # The user-supplied description of the Snapshot.
    size: int  # The snapshot size in bytes.
    status: str  # The Snapshot status, see `enums.SnapshotStatus` for possible values.
    os_id: int  # The Operating System id, check OperatingSystemAPI.list and `OSItem.id` for available OSes.
    app_id: int  # The Application id, check `Application.list` and `ApplicationItem.id` for available options.


class SnapshotAPI(BaseVultrV2):
    """Vultr Snapshot API.

    Reference: https://www.vultr.com/api/#tag/snapshot

    A snapshot is a point-in-time image of an instance. We do not stop the instance when taking a snapshot.
    Booting from a snapshot is similar to rebooting after a non-graceful restart. Snapshots are physically the
    same as backups, but snapshots are manual while backups run automatically on a schedule.
    See our Snapshot Quickstart Guide for more information.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "snapshots")

    @command
    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[Snapshot]:
        """Get information about all Snapshots in your account.

        Args:
            per_page: number of items requested per page. Default is 100 and Max is 500.
            cursor: cursor for paging.
            capacity: The capacity of the VultrPagination[SnapshotItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[Snapshot]: A list-like object of `SnapshotItem` object.
        """
        return VultrPagination[Snapshot](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=Snapshot,
            capacity=capacity,
        )

    @command
    def create(self, instance_id: str, description: str = None) -> Snapshot:
        """Create a new Snapshot for `instance_id`.

        Args:
            instance_id: Create a Snapshot for this `instance_id`.
            description: The user-supplied description of the Snapshot.

        Returns:
            Snapshot: The Snapshot object.
        """
        _json = {
            "instance_id": instance_id,
            "description": description,
        }
        resp = self._post(json=_json)
        return Snapshot.from_dict(get_only_value(resp))

    @command
    def create_from_url(self, url: str) -> Snapshot:
        """Create a new Snapshot from a RAW image located at `url`.

        Args:
            url: The public URL containing a RAW image.

        Returns:
            Snapshot: The Snapshot object.
        """
        _json = {
            "url": url,
        }
        resp = self._post("/create-from-url", json=_json)
        return Snapshot.from_dict(get_only_value(resp))

    @command
    def get(self, snapshot_id: str) -> Snapshot:
        """Get information about a Snapshot.

        Args:
            snapshot_id: The Snapshot ID.

        Returns:
            Snapshot: The Snapshot object.
        """
        resp = self._get(f"/{snapshot_id}")
        return Snapshot.from_dict(get_only_value(resp))

    @command
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

    @command
    def delete(self, snapshot_id: str):
        """Delete a Snapshot.

        Args:
            snapshot_id: The Snapshot ID.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{snapshot_id}")
