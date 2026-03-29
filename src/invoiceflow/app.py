import logging
import os

from openai import OpenAI

from invoiceflow.config.settings import settings
from invoiceflow.config.logger import setup_logging
from invoiceflow.models.invoice import ERPDetails, Invoice, InvoiceStatus
from invoiceflow.models.queue_message import ServiceBusMessage
from invoiceflow.prompt.loader import ChatModelPrompt, load_prompt_messages
from invoiceflow.services.erp_client import match_invoice_with_erp
from invoiceflow.services.llm_extractor import process_invoice_as_images, process_invoice_as_text
from invoiceflow.services.openai_client import init_openai_client
from invoiceflow.services.outbound_router import route
from invoiceflow.services.service_bus_consumer import load_message, get_service_bus_message
from invoiceflow.services.validator import validate

logger = logging.getLogger(__name__)

def _process_message(queue_message: ServiceBusMessage, openai_client: OpenAI, prompt_message: ChatModelPrompt) -> Invoice:
    if queue_message.is_scan:
        invoice = process_invoice_as_images(
            attachment_base64=queue_message.image_b64encoded,
            openai_client=openai_client,
            openai_model=settings.azure_openai_model,
            prompt_messages=prompt_message
        )
    else:
        invoice = process_invoice_as_text(
            text=queue_message.invoice_content,
            openai_client=openai_client,
            openai_model=settings.azure_openai_model,
            prompt_messages=prompt_message
        )
    logger.info("invoice information extracted")

    return invoice


def _validate_invoice(invoice: Invoice) -> Invoice:
    logger.info("validating invoice information")
    validation_errors = validate(invoice)

    if validation_errors:
        invoice.status = InvoiceStatus.MANUAL_REVIEW
        logger.warning(
            f"Invoice {invoice.invoice_number} flagged for manual review: "
            f"{validation_errors}"
        )
    else:
        invoice.status = InvoiceStatus.VALIDATED
        logger.info(f"Invoice {invoice.invoice_number} validated successfully.")

    return invoice
    

def _erp_match(invoice: Invoice) -> ERPDetails:
    return match_invoice_with_erp(invoice=invoice)

def run():
    setup_logging()
    openai_client = init_openai_client(api_key=settings.azure_openai_api_key)
    prompt_message = load_prompt_messages(prompt_files_path=settings.prompt_path, version=settings.prompt_version)
    logger.info("invoiceflow ready")

    messages = get_service_bus_message(settings.example_data)

    for message in messages:
        queue_message = load_message(message)
        invoice = _process_message(queue_message=queue_message, openai_client=openai_client, prompt_message=prompt_message)
        invoice = _validate_invoice(invoice=invoice)
        erp_details = _erp_match(invoice=invoice)

        route(invoice, erp_details, queue_message)




if __name__ == "__main__":
    run()