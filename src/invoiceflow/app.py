import logging
import os

from invoiceflow.config.settings import settings
from invoiceflow.config.logger import setup_logging
from invoiceflow.prompt.loader import load_prompt_messages
from invoiceflow.services.llm_extractor import process_invoice_as_images, process_invoice_as_text
from invoiceflow.services.openai_client import init_openai_client
from invoiceflow.services.service_bus_consumer import load_message, get_service_bus_message

logger = logging.getLogger(__name__)

def run():
    setup_logging()
    logger.info("starting invoiceflow...")
    openai_client = init_openai_client(api_key=settings.azure_openai_api_key)
    prompt_message = load_prompt_messages(prompt_files_path=settings.prompt_path, version=settings.prompt_version)
    logger.info("invoiceflow ready")

    messages = get_service_bus_message(settings.example_data)

    for message in messages:
        queue_message = load_message(message)

        logger.info("processing new message...")
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


if __name__ == "__main__":
    run()