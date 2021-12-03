from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value

from .base import BaseVultrV2, command
from .enums import StartupScriptType


@dataclass
class StartupScript(BaseDataclass):
    id: str  # A unique ID for the Startup Script.
    date_created: str  # The date the Startup Script was created.
    date_modified: str  # The date the Startup Script was last modified.
    name: str  # The user-supplied name of the Startup Script.
    type: str  # The Startup Script type,, see `enums.StartupScriptType` for possible values.
    script: str = None  # The base-64 encoded Startup Script.


class StartupScriptAPI(BaseVultrV2):
    """Vultr StartupScript API.

    Reference: https://www.vultr.com/api/#tag/startup

    Vultr allows you to assign two types of scripts to a server.
    Boot scripts configure new deployments, and PXE scripts automatically install operating systems.
    Assign startup scripts to your servers through the API or on your Startup Scripts page in the customer portal.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "startup-scripts")

    @command
    def list(
        self,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[StartupScript]:
        """Get a list of all Startup Scripts.

        Args:
            per_page: number of items requested per page. Default is 100 and Max is 500.
            cursor: cursor for paging.
            capacity: The capacity of the VultrPagination[StartupScriptItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[StartupScript]: A list-like object of `StartupScriptItem` object.

        """
        return VultrPagination[StartupScript](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=StartupScript,
            capacity=capacity,
        )

    @command
    def create(self, name: str, script: str, script_type: StartupScriptType = None) -> StartupScript:
        """Create a new Startup Script.

        The `name` and `script` attributes are required, and scripts are base-64 encoded.

        Args:
            name: The name of the Startup Script.
            script: The base-64 encoded Startup Script.
            script_type: The Startup Script type.

        Returns:
            StartupScript: The Startup Script item.
        """
        _json = {
            "name": name,
            "script": script,
            "type": script_type and script_type.value,
        }
        resp = self._post(json=_json)
        return StartupScript.from_dict(data=get_only_value(resp))

    @command
    def get(self, startup_id: str) -> StartupScript:
        """Get information for a Startup Script.

        Args:
            startup_id: The Startup Script id.

        Returns:
            StartupScript: The Startup Script item.
        """
        resp = self._get(f"/{startup_id}")
        return StartupScript.from_dict(data=get_only_value(resp))

    @command
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

    @command
    def delete(self, startup_id: str):
        """Delete a Startup Script.

        Args:
            startup_id: Startup Script id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{startup_id}")
