import logging

from invoiceflow.models.invoice import Invoice
from invoiceflow.models.erp_detail import ERPDetails
from invoiceflow.models.queue_message import ServiceBusMessage


logger = logging.getLogger(__name__)


def route(
    invoice: Invoice, erp_details: ERPDetails, queue_message: ServiceBusMessage
) -> None:
    logger.info(
        f"Routing invoice: {invoice.invoice_number} — status: {invoice.validation_status.status} and erp match: {erp_details.status}"
    )
