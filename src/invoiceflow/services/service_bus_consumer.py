import base64
from io import BytesIO
import logging
import datetime
import os

import PyPDF2
import fitz

from invoiceflow.models.queue_message import ServiceBusMessage


logger = logging.getLogger(__name__)


def get_service_bus_message(pdf_folder_path: str) -> str:
    """
    Simulates next service bus queue message as b64 encoded string

    :param pdf_path: path to pdf
    :return: b64 encoded string
    """

    list_pdf_bytes = []

    for file_name in os.listdir(pdf_folder_path):
        file_path = os.path.join(pdf_folder_path, file_name)

        with open(file_path, "rb") as f:
            pdf_bytes = f.read()

        list_pdf_bytes.append(base64.b64encode(pdf_bytes))

    return list_pdf_bytes


def load_message(queue_message: str) -> ServiceBusMessage:
    """
    Process messages from service bus queue and extracts information from pdf or email body

    :param queue_message: service bus queue message
    :return: service bus message information
    """
    logger.info("incoming message from service bus queue...")

    pdf_bytes = base64.b64decode(queue_message)

    is_scan = False
    text = ""
    image_bytes = bytes()
    reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))

    for page in reader.pages:
        text += page.extract_text() or ""

    # check if pdf is available as scan or text
    if len(text.strip()) == 0:
        # pdf is available as scan
        # pdf gets converted to image to process image with llm
        is_scan = True

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in doc:
            pix = page.get_pixmap()
            image_bytes = pix.tobytes("png", 100)

    return ServiceBusMessage(
        invoice_content = text,
        image_b64encoded=base64.b64encode(image_bytes),
        received_at=datetime.datetime.now().isoformat(),
        is_scan=is_scan
    )