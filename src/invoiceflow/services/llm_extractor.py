import logging

from invoiceflow.models.invoice import Invoice
from openai import OpenAI

from invoiceflow.prompt.loader import ChatModelPrompt

logger = logging.getLogger(__name__)

def process_invoice_as_text(
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


def process_invoice_as_images(
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
