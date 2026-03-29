import logging

from invoiceflow.models.invoice import Invoice, InvoiceStatus

logger = logging.getLogger(__name__)


def validate(invoice: Invoice) -> Invoice:
    validation_errors = []

    for item in invoice.line_items:
        expected = round(item.quantity * item.unit_price, 2)
        if abs(expected - item.amount_net) > 0.02:
            validation_errors.append(
                f"Line item amount mismatch for '{item.description}': "
                f"expected {expected}, got {item.amount_net}."
            )

    if invoice.amount_net + invoice.amount_vat_10 + invoice.amount_vat_20 != invoice.amount_gross:
        validation_errors.append(
                f"Total amount mismatch: "
                f"expected {invoice.amount_gross}, got {invoice.amount_net + invoice.amount_vat_10 + invoice.amount_vat_20}."
            )

    return validation_errors