import logging

from invoiceflow.models.invoice import ERPDetails, Invoice
from invoiceflow.models.queue_message import ServiceBusMessage


logger = logging.getLogger(__name__)

def route(invoice: Invoice, erp_details: ERPDetails, queue_message: ServiceBusMessage) -> None:
    logger.info(f"Routing invoice: {invoice.invoice_number} — status: {invoice.status}")