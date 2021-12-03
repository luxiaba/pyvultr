from dataclasses import dataclass
from functools import partial
from typing import Optional
from urllib.parse import urljoin

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value

from .base import BaseVultrV2, command


@dataclass
class Bill(BaseDataclass):
    id: int  # ID of the billing history item.
    date: str  # Date billing history item was generated.
    type: str  # Type of billing history item.
    description: str  # Description of billing history item.
    amount: float  # Amount for the billing history item in dollars.
    balance: float  # The accounts balance in dollars.


@dataclass
class Invoice(BaseDataclass):
    id: int  # ID of the invoice.
    date: str  # Date the invoice was generated.
    description: str  # Description of the invoice.
    amount: float  # Amount of the invoice in dollars.
    balance: float  # The accounts balance in dollars.


@dataclass
class InvoiceItem(BaseDataclass):
    description: str  # Description of the invoice item.
    end_date: str  # End date of item.
    product: str  # Product name.
    start_date: str  # Start date of item.
    total: float  # Total amount due in dollars.
    unit_price: float  # Price per unit in dollars.
    unit_type: str  # Unit type, see `enums.InvoiceUnitType` for details.
    units: int  # Number of units item consumed in billing period.


class BillingAPI(BaseVultrV2):
    """Vultr Billing API.

    Reference: https://www.vultr.com/api/#tag/billing

    Read-only billing information for your user account.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self) -> str:
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "billing")

    @command
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

    @command
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

    @command
    def get_invoice(self, invoice_id: str) -> Invoice:
        """Retrieve specified invoice.

        Args:
            invoice_id: The Invoice ID.

        Returns:
            Invoice: A `Invoice` object.
        """
        resp = self._get(f"/invoices/{invoice_id}")
        return Invoice.from_dict(get_only_value(resp))

    @command
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
