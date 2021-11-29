from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

import dacite

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value
from pyvultr.v2.base import BaseVultrV2


@dataclass
class SSHKeyItem(BaseDataclass):
    id: str
    date_created: str
    name: str
    ssh_key: str


class SSHKey(BaseVultrV2):
    """Vultr SSHKey API.

    You can add SSH keys to your account, which can be copied to new instances when first deployed.
    Updating a key does not update any running instances.
    If you reinstall an instance (erasing all its data), it will inherit the updated key.

    Attributes:
        api_key: Vultr API key, we get it from env variable `VULTR_API_TOKEN` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "ssh-keys")

    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[SSHKeyItem]:
        """List all SSH Keys in your account.

        Args:
            per_page: number of items requested per page. Default is 100 and Max is 500.
            cursor: cursor for paging.
            capacity: the capacity of the VultrPagination[SSHKeyItem],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[SSHKeyItem]: A paginated list of `SSHKeyItem`.
        """
        return VultrPagination[SSHKeyItem](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=SSHKeyItem,
            capacity=capacity,
        )

    def create(self, name: str, ssh_key: str) -> SSHKeyItem:
        """Create a new SSH Key for use with future instances.

        This does not update any running instances.

        Args:
            name: The user-supplied name for this SSH Key.
            ssh_key: The SSH Key.

        Returns:
            SSHKeyItem: The SSH Key.
        """
        _json = {
            "name": name,
            "ssh_key": ssh_key,
        }
        resp = self._post(json=_json)
        return dacite.from_dict(data_class=SSHKeyItem, data=get_only_value(resp))

    def get(self, ssh_key_id: str) -> SSHKeyItem:
        """Get information about an SSH Key.

        Args:
            ssh_key_id: The SSH Key ID.

        Returns:
            SSHKeyItem: The SSH Key.
        """
        resp = self._get(f"/{ssh_key_id}")
        return dacite.from_dict(data_class=SSHKeyItem, data=get_only_value(resp))

    def update(self, ssh_key_id: str, name: str = None, ssh_key: str = None):
        """Update an SSH Key.

        The attributes name and ssh_key are optional.
        If not set, the attributes will retain their original values.
        New deployments will use the updated key, but this action does not update previously deployed instances.

        Args:
            ssh_key_id: The SSH Key ID.
            name: The user-supplied name for this SSH Key.
            ssh_key: The SSh Key.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "name": name,
            "ssh_key": ssh_key,
        }
        return self._put(f"/{ssh_key_id}", json=_json)

    def delete(self, ssh_key_id: str):
        """Delete an SSH Key.

        Args:
            ssh_key_id: The SSH Key ID.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{ssh_key_id}")
