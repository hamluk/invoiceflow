import logging

from invoiceflow.models.invoice import Invoice, InvoiceStatus

logger = logging.getLogger(__name__)


def _validate_invoice(invoice: Invoice) -> Invoice:
    validation_errors = []

    for item in invoice.line_items:
        expected = round(item.quantity * item.unit_price, 2)
        if expected != item.amount_net:
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


def validate_invoice_details(invoice: Invoice) -> Invoice:
    logger.info("validating invoice information")
    validation_errors = _validate_invoice(invoice)

    if validation_errors:
        invoice.validation_status.status = InvoiceStatus.MANUAL_REVIEW
        invoice.validation_status.validation_errors = validation_errors
        logger.warning(
            f"Invoice {invoice.invoice_number} flagged for manual review: "
            f"{validation_errors}"
        )
    else:
        invoice.validation_status.status = InvoiceStatus.VALIDATED
        logger.info(f"Invoice {invoice.invoice_number} validated successfully.")

    return invoice