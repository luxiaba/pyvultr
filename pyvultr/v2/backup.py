from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value

from .base import BaseVultrV2, command


@dataclass
class Backup(BaseDataclass):
    id: str  # A unique ID for the backup.
    date_created: str  # The date the backup was created.
    description: str  # The user-supplied description of this backup.
    size: int  # The size of the backup in Bytes.
    status: str  # The Backup status, see `enums.BackupStatus` for details.


class BackupAPI(BaseVultrV2):
    """Vultr Backup API.

    Reference: https://www.vultr.com/api/#tag/backup

    A backup is a scheduled, automatic, point-in-time image of an instance.
    We do not stop the instance when taking a backup. Booting from a backup is similar to rebooting
    after a non-graceful restart. Snapshots are physically the same as backups, but snapshots are manual while
    backups run automatically on a schedule.
    Backups can be converted into snapshots. See our Automatic Backup FAQ for more information.

    Attributes
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided..
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "backups")

    @command
    def list(
        self,
        per_page: int = None,
        cursor: str = None,
        instance_id: str = None,
        capacity: int = None,
    ) -> VultrPagination[Backup]:
        """Get information about Backups in your account. You can filter the list by `instance_id`.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            instance_id: Filter the backup list by Instance id.
            capacity: The capacity of the VultrPagination[BackupItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[Backup]: A list-like object of `BackupItem` object.
        """
        extra_params = {
            "instance_id": instance_id,
        }
        return VultrPagination[Backup](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=Backup,
            capacity=capacity,
            **extra_params,
        )

    @command
    def get(self, backup_id: str) -> Backup:
        """Get the information for the Backup.

        Args:
            backup_id: The Backup ID.

        Returns:
            Backup: A `BackupItem` object.
        """
        resp = self._get(f"/{backup_id}")
        return Backup.from_dict(data=get_only_value(resp))
