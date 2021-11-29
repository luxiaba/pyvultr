from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

import dacite

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value
from pyvultr.v2.base import BaseVultrV2


@dataclass
class BackupItem(BaseDataclass):
    id: str
    date_created: str
    description: str
    size: int
    status: str


class Backup(BaseVultrV2):
    """Vultr Backup API.

    A backup is a scheduled, automatic, point-in-time image of an instance.
    We do not stop the instance when taking a backup. Booting from a backup is similar to rebooting
    after a non-graceful restart. Snapshots are physically the same as backups, but snapshots are manual while
    backups run automatically on a schedule.
    Backups can be converted into snapshots. See our Automatic Backup FAQ for more information.

    Attributes
        api_key: Vultr API key, we get it from env variable `VULTR_API_TOKEN` if not provided..
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "backups")

    def list(
        self,
        per_page: int = None,
        cursor: str = None,
        instance_id: str = None,
        capacity: int = None,
    ) -> VultrPagination[BackupItem]:
        """Get information about Backups in your account. You can filter the list by `instance_id`.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            instance_id: Filter the backup list by Instance id.
            capacity: the capacity of the VultrPagination[BackupItem],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[BackupItem]: a paginated list of `BackupItem`.
        """
        extra_params = {
            "instance_id": instance_id,
        }
        return VultrPagination[BackupItem](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=BackupItem,
            capacity=capacity,
            **extra_params,
        )

    def get(self, backup_id: str) -> BackupItem:
        """Get the information for the Backup.

        Args:
            backup_id: The Backup ID.

        Returns:
            BackupItem: A `BackupItem` object.
        """
        resp = self._get(f"/{backup_id}")
        return dacite.from_dict(data_class=BackupItem, data=get_only_value(resp))
