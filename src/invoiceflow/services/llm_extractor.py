import logging

from invoiceflow.config.settings import Settings
from invoiceflow.models.invoice import Invoice
from openai import OpenAI

from invoiceflow.models.queue_message import ServiceBusMessage
from invoiceflow.prompt.loader import ChatModelPrompt

logger = logging.getLogger(__name__)

def _process_invoice_as_text(
    text: str,
    openai_client: OpenAI,
    openai_model: str,
    prompt_messages: ChatModelPrompt) -> Invoice:
    response = openai_client.responses.parse(
        model = openai_model,
        input=[
            {
                "role": "system",
                "content": prompt_messages.system
            },
            {
                "role": "user",
                "content": prompt_messages.user + text
            }
        ],
        text_format=Invoice
    )
    return response.output_parsed


def _process_invoice_as_images(
        attachment_base64: str,
        openai_client: OpenAI,
        openai_model: str,
        prompt_messages: ChatModelPrompt) -> Invoice:
    response = openai_client.responses.parse(
        model = openai_model,
        input=[
            {
                "role": "system",
                "content": prompt_messages.system
            },
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": prompt_messages.user },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{attachment_base64}",
                    },
                ],
            }
        ],
        text_format=Invoice
    )  

    return response.output_parsed


def process_message(settings: Settings, queue_message: ServiceBusMessage, openai_client: OpenAI, prompt_message: ChatModelPrompt) -> Invoice:
    if queue_message.is_scan:
        invoice = _process_invoice_as_images(
            attachment_base64=queue_message.image_b64encoded,
            openai_client=openai_client,
            openai_model=settings.azure_openai_model,
            prompt_messages=prompt_message
        )
    else:
        invoice = _process_invoice_as_text(
            text=queue_message.invoice_content,
            openai_client=openai_client,
            openai_model=settings.azure_openai_model,
            prompt_messages=prompt_message
        )
    logger.info("invoice information extracted")

    return invoice
