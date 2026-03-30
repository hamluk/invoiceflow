import logging

from invoiceflow.config.settings import settings
from invoiceflow.config.logger import setup_logging
from invoiceflow.prompt.loader import load_prompt_messages
from invoiceflow.services.erp_client import erp_match
from invoiceflow.services.llm_extractor import process_message
from invoiceflow.services.openai_client import init_openai_client
from invoiceflow.services.outbound_router import route
from invoiceflow.services.service_bus_consumer import load_message, get_service_bus_message
from invoiceflow.services.validator import validate_invoice_details

logger = logging.getLogger(__name__)


def run():
    setup_logging()
    openai_client = init_openai_client(api_key=settings.azure_openai_api_key)
    prompt_message = load_prompt_messages(prompt_files_path=settings.prompt_path, version=settings.prompt_version)
    logger.info("invoiceflow ready")

    messages = get_service_bus_message(settings.example_data)

    for message in messages:
        queue_message = load_message(message)
        invoice = process_message(settings=settings, queue_message=queue_message, openai_client=openai_client, prompt_message=prompt_message)
        invoice = validate_invoice_details(invoice=invoice)
        erp_details = erp_match(invoice=invoice)

        route(invoice, erp_details, queue_message)
