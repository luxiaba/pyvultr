from dataclasses import dataclass
from functools import partial
from typing import Optional

from pyvultr.utils import BaseDataclass, VultrPagination
from pyvultr.v2.base import BaseVultrV2
from pyvultr.v2.enum import ApplicationType


@dataclass
class ApplicationItem(BaseDataclass):
    deploy_name: str
    id: int
    image_id: str
    name: str
    short_name: str
    type: str
    vendor: str


class Application(BaseVultrV2):
    """Vultr Application API.

    One-Click and Marketplace Applications are ready-to-run with minimal configuration.
    We have an extensive documentation library for our Applications.

    There are two types of Applications: marketplace and one-click.
    This is denoted by the type field in the Application object.
    Applications with type of marketplace can be deployed by using the image_id
    while Applications with type of one-click should use the id.

    Attributes:
        api_key: Vultr API key, we get it from env variable `VULTR_API_TOKEN` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    def list(
        self,
        per_page: int = None,
        cursor: str = None,
        app_type: ApplicationType = None,
        capacity: int = None,
    ) -> VultrPagination[ApplicationItem]:
        """Get a list of all available Applications. This list can be filtered by `app_type`.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            app_type: Filter the results by type.
            capacity: the capacity of the VultrPagination[ApplicationItem],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[ApplicationItem]: a paginated list of `ApplicationItem`.
        """
        extra_params = {
            "type": app_type and app_type.value,
        }
        fetcher = partial(self._get, endpoint="/applications")
        return VultrPagination[ApplicationItem](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=ApplicationItem,
            capacity=capacity,
            **extra_params,
        )
