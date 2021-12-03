from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value

from .base import BaseVultrV2, command


@dataclass
class SSHKey(BaseDataclass):
    id: str  # A unique ID for the SSH Key.
    date_created: str  # The date this SSH Key was created.
    name: str  # The user-supplied name for this SSH Key.
    ssh_key: str  # The SSH Key.


class SSHKeyAPI(BaseVultrV2):
    """Vultr SSHKey API.

    Reference: https://www.vultr.com/api/#tag/ssh

    You can add SSH keys to your account, which can be copied to new instances when first deployed.
    Updating a key does not update any running instances.
    If you reinstall an instance (erasing all its data), it will inherit the updated key.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "ssh-keys")

    @command
    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[SSHKey]:
        """List all SSH Keys in your account.

        Args:
            per_page: number of items requested per page. Default is 100 and Max is 500.
            cursor: cursor for paging.
            capacity: The capacity of the VultrPagination[SSHKeyItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[SSHKey]: A list-like object of `SSHKeyItem` object.
        """
        return VultrPagination[SSHKey](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=SSHKey,
            capacity=capacity,
        )

    @command
    def create(self, name: str, ssh_key: str) -> SSHKey:
        """Create a new SSH Key for use with future instances.

        This does not update any running instances.

        Args:
            name: The user-supplied name for this SSH Key.
            ssh_key: The SSH Key.

        Returns:
            SSHKey: The SSH Key.
        """
        _json = {
            "name": name,
            "ssh_key": ssh_key,
        }
        resp = self._post(json=_json)
        return SSHKey.from_dict(get_only_value(resp))

    @command
    def get(self, ssh_key_id: str) -> SSHKey:
        """Get information about an SSH Key.

        Args:
            ssh_key_id: The SSH Key ID.

        Returns:
            SSHKey: The SSH Key.
        """
        resp = self._get(f"/{ssh_key_id}")
        return SSHKey.from_dict(get_only_value(resp))

    @command
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

    @command
    def delete(self, ssh_key_id: str):
        """Delete an SSH Key.

        Args:
            ssh_key_id: The SSH Key ID.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{ssh_key_id}")
