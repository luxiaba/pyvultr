from dataclasses import dataclass
from functools import partial
from typing import Optional
from urllib.parse import urljoin

import dacite

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value

from .base import BaseVultrV2


@dataclass
class Bill(BaseDataclass):
    id: int
    date: str
    type: str
    description: str
    amount: float
    balance: float


@dataclass
class Invoice(BaseDataclass):
    id: int
    date: str
    description: str
    amount: float
    balance: float


@dataclass
class InvoiceItem(BaseDataclass):
    description: str
    end_date: str
    product: str
    start_date: str
    total: float
    unit_price: float
    unit_type: str
    units: int


class Billing(BaseVultrV2):
    """Vultr Billing API.

    Reference: https://www.vultr.com/zh/api/#tag/billing

    Read-only billing information for your user account.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$ENV_TOKEN_NAME` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self) -> str:
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "billing")

    def list_bills(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[Bill]:
        """Retrieve list of billing history.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: The capacity of the VultrPagination[Bill], see `VultrPagination` for details.

        Returns:
            VultrPagination[Bill]: A list-like object of `Bill` object.
        """
        fetcher = partial(self._get, endpoint="/history")
        return VultrPagination[Bill](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=Bill,
            capacity=capacity,
        )

    def list_invoices(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[Invoice]:
        """Retrieve full specified invoice.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: The capacity of the VultrPagination[Invoice], see `VultrPagination` for details.

        Returns:
            VultrPagination[Invoice]: A list-like object of `Invoice` object.
        """
        fetcher = partial(self._get, endpoint="/invoices")
        return VultrPagination[Invoice](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=Invoice,
            capacity=capacity,
        )

    def get_invoice(self, invoice_id: str) -> Invoice:
        """Retrieve specified invoice.

        Args:
            invoice_id: The Invoice ID.

        Returns:
            Invoice: A `Invoice` object.
        """
        resp = self._get(f"/invoices/{invoice_id}")
        return dacite.from_dict(data_class=Invoice, data=get_only_value(resp))

    def list_invoice_items(
        self,
        invoice_id: str,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[InvoiceItem]:
        """Retrieve full specified invoice.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            invoice_id: The Invoice ID.
            capacity: The capacity of the VultrPagination[InvoiceItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[InvoiceItem]: A list-like object of `InvoiceItem` object.
        """
        fetcher = partial(self._get, endpoint=f"/invoices/{invoice_id}/items")
        return VultrPagination[InvoiceItem](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=InvoiceItem,
            capacity=capacity,
        )
