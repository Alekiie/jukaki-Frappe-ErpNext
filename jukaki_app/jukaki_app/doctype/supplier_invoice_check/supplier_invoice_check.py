# Copyright (c) 2026, Alexander and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from datetime import datetime


class SupplierInvoiceCheck(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        amount: DF.Currency
        due_date: DF.Date
        invoice_date: DF.Date
        invoice_number: DF.Data
        status: DF.Literal["Draft", "Verified", "Rejected"]
        supplier: DF.Link
        vat_amount: DF.Currency
    # end: auto-generated types

    def validate(self):
        self.validate_amount()
        self.validate_dates()
        self.validate_duplicate_invoices()

    def validate_amount(self):
        if self.amount is None or self.amount <= 0:
            frappe.throw(
                _("Amount must be greater than zero.Please try a higher amount")
            )

    def validate_dates(self):
        if self.invoice_date and self.due_date and self.due_date < self.invoice_date:
            frappe.throw(_("Due Date cannot be before the Invoice date"))

    def validate_duplicate_invoices(self):
        if not self.supplier or not self.invoice_number:
            return
        duplicate = frappe.db.exists(
            "Supplier Invoice Check",
            {
                "supplier": self.supplier,
                "invoice_number": self.invoice_number,
                "name": ["!=", self.name],
            },
        )
        if duplicate:
            frappe.throw(
                _("Invoice {0} already exists from supplier {1}").format(
                    self.invoice_number, self.supplier
                )
            )

    _DOCTYPE_NAME = "Supplier Invoice Check"
