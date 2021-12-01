from pyvultr.base_api import SupportHttpMethod
from pyvultr.v2 import Bill, Invoice, InvoiceItem
from tests.v2 import BaseTestV2


class TestBilling(BaseTestV2):
    def test_list_bills(self):
        """Test list bills."""
        with self._get("response/billing") as mock:
            _excepted_result = mock.python_body["billing_history"][0]
            excepted_result = Bill.from_dict(_excepted_result)

            _real_result = self.api_v2.billing.list_bills()
            real_result: Bill = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/billing/history")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_list_invoices(self):
        """Test list invoices."""
        with self._get("response/billing_invoices") as mock:
            _excepted_result = mock.python_body["billing_invoices"][0]
            excepted_result = Invoice.from_dict(_excepted_result)

            _real_result = self.api_v2.billing.list_invoices()
            real_result: Invoice = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/billing/invoices")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_get_invoice(self):
        """Test get invoice."""
        with self._get("response/billing_invoice", expected_returned=Invoice) as mock:
            excepted_result = mock.python_body

            invoice_id = "734923"
            real_result: Invoice = self.api_v2.billing.get_invoice(invoice_id=invoice_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/billing/invoices/{invoice_id}")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_list_invoice_items(self):
        """Test list invoice items."""
        with self._get("response/billing_invoice_items") as mock:
            _excepted_result = mock.python_body["invoice_items"][0]
            excepted_result = InvoiceItem.from_dict(_excepted_result)

            invoice_id = "4829212"
            _real_result = self.api_v2.billing.list_invoice_items(invoice_id=invoice_id)
            real_result: InvoiceItem = _real_result.first()

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/billing/invoices/{invoice_id}/items")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)
