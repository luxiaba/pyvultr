from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

import dacite

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value
from pyvultr.v2.base import BaseVultrV2
from pyvultr.v2.enum import StartupScriptType


@dataclass
class StartupScriptItem(BaseDataclass):
    id: str
    date_created: str
    date_modified: bool
    name: str
    script: str
    type: str


class StartupScript(BaseVultrV2):
    """Vultr StartupScript API.

    Vultr allows you to assign two types of scripts to a server.
    Boot scripts configure new deployments, and PXE scripts automatically install operating systems.
    Assign startup scripts to your servers through the API or on your Startup Scripts page in the customer portal.

    Attributes:
        api_key: Vultr API key, we get it from env variable `VULTR_API_TOKEN` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "startup-scripts")

    def list(
        self,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[StartupScriptItem]:
        """Get a list of all Startup Scripts.

        Args:
            per_page: number of items requested per page. Default is 100 and Max is 500.
            cursor: cursor for paging.
            capacity: the capacity of the VultrPagination[StartupScriptItem],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[StartupScriptItem]

        """
        return VultrPagination[StartupScriptItem](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=StartupScriptItem,
            capacity=capacity,
        )

    def create(self, name: str, script: str, script_type: StartupScriptType = None) -> StartupScriptItem:
        """Create a new Startup Script.

        The `name` and `script` attributes are required, and scripts are base-64 encoded.

        Args:
            name: The name of the Startup Script.
            script: The base-64 encoded Startup Script.
            script_type: The Startup Script type.

        Returns:
            StartupScriptItem: The Startup Script item.
        """
        _json = {
            "name": name,
            "script": script,
            "type": script_type and script_type.value,
        }
        resp = self._post(json=_json)
        return dacite.from_dict(data_class=StartupScriptItem, data=get_only_value(resp))

    def get(self, startup_id: str) -> StartupScriptItem:
        """Get information for a Startup Script.

        Args:
            startup_id: The Startup Script id.

        Returns:
            StartupScriptItem: The Startup Script item.
        """
        resp = self._get(f"/{startup_id}")
        return dacite.from_dict(data_class=StartupScriptItem, data=get_only_value(resp))

    def update(self, startup_id: str, name: str = None, script: str = None, script_type: StartupScriptType = None):
        """Update a Startup Script.

        The attributes name and script are optional.
        If not set, the attributes will retain their original values. The script attribute is base-64 encoded.
        New deployments will use the updated script, but this action does not update previously deployed instances.

        Args:
            startup_id: Startup Script id.
            name: The name of the Startup Script.
            script: The base-64 encoded Startup Script.
            script_type: The Startup Script type.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "name": name,
            "script": script,
            "type": script_type and script_type.value,
        }
        return self._patch(f"/{startup_id}", json=_json)

    def delete(self, startup_id: str):
        """Delete a Startup Script.

        Args:
            startup_id: Startup Script id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{startup_id}")
