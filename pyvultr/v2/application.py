from dataclasses import dataclass
from functools import partial
from typing import Optional

from pyvultr.utils import BaseDataclass, VultrPagination

from .base import BaseVultrV2, command
from .enums import ApplicationType


@dataclass
class Application(BaseDataclass):
    id: int  # A unique ID for the application.
    name: str  # The application name.
    short_name: str  # The short application name.
    deploy_name: str  # A long description of the application.
    vendor: str  # The application vendor name.
    image_id: str  # A unique ID for marketplace applications.
    type: str  # The type of application, see `enums.ApplicationType` for details.


class ApplicationAPI(BaseVultrV2):
    """Vultr Application API.

    Reference: https://www.vultr.com/api/#tag/application

    One-Click and Marketplace Applications are ready-to-run with minimal configuration.
    We have an extensive documentation library for our Applications.

    There are two types of Applications: marketplace and one-click.
    This is denoted by the type field in the Application object.
    Applications with type of marketplace can be deployed by using the image_id
    while Applications with type of one-click should use the id.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @command
    def list(
        self,
        per_page: int = None,
        cursor: str = None,
        app_type: ApplicationType = None,
        capacity: int = None,
    ) -> VultrPagination[Application]:
        """Get a list of all available Applications. This list can be filtered by `app_type`.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            app_type: Filter the results by type.
            capacity: The capacity of the VultrPagination[ApplicationItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[Application]: A list-like object of `ApplicationItem` object.
        """
        extra_params = {
            "type": app_type and app_type.value,
        }
        fetcher = partial(self._get, endpoint="/applications")
        return VultrPagination[Application](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=Application,
            capacity=capacity,
            **extra_params,
        )
