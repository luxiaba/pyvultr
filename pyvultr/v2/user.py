from dataclasses import dataclass
from typing import List, Optional
from urllib.parse import urljoin

import dacite

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value
from pyvultr.v2.base import BaseVultrV2
from pyvultr.v2.enum import ACL


@dataclass
class UserInfo(BaseDataclass):
    id: str
    name: str
    api_enabled: bool
    email: str
    password: str
    acls: List[str]


class User(BaseVultrV2):
    """Vultr User API.

    Vultr supports multiple users in each account, and each user has individual access permissions.
    Users have unique API keys, which respect the permission for that user.

    Attributes:
        api_key: Vultr API key, we get it from env variable `VULTR_API_TOKEN` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "users")

    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[UserInfo]:
        """Get a list of all Users in your account.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: The capacity of the VultrPagination[UserInfo],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[UserInfo]: A paginated list of User info.
        """
        return VultrPagination[UserInfo](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=UserInfo,
            capacity=capacity,
        )

    def create(
        self,
        name: str,
        email: str,
        password: str,
        api_enabled: bool = None,
        acl_group: List[ACL] = None,
    ) -> UserInfo:
        """Create a new User. The `email`, `name`, and `password` attributes are required.

        Args:
            name: The User's name.
            email: The User's email address.
            password: The User's password.
            api_enabled: API access is permitted for this User.
            acl_group: An array of permission granted.

        Returns:
            UserInfo: User info.
        """
        _json = {
            "name": name,
            "email": email,
            "password": password,
            "api_enabled": api_enabled,
            "acls": acl_group and [i.value for i in acl_group],
        }
        resp = self._post(json=_json)
        return dacite.from_dict(data_class=UserInfo, data=get_only_value(resp))

    def get(self, user_id: str) -> UserInfo:
        """Get information about a User.

        Args:
            user_id: The User id.

        Returns:
            UserInfo: User info.
        """
        resp = self._get(f"/{user_id}")
        return dacite.from_dict(data_class=UserInfo, data=get_only_value(resp))

    def update(
        self,
        user_id: str,
        name: str = None,
        email: str = None,
        password: str = None,
        api_enabled: bool = None,
        acl_group: List[ACL] = None,
    ):
        """Update information for a User.

        All attributes are optional. If not set, the attributes will retain their original values.

        Args:
            user_id: The User id.
            name: The User's name.
            email: The User's email address.
            password: The User's password.
            api_enabled: API access is permitted for this User.
            acl_group: An array of permission granted.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "name": name,
            "email": email,
            "password": password,
            "api_enabled": api_enabled,
            "acls": acl_group and [i.value for i in acl_group],
        }
        return self._patch(f"/{user_id}", json=_json)

    def delete(self, user_id: str):
        """Delete a User.

        Args:
            user_id: Ths User id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{user_id}")
