from pydantic import BaseModel
from typing import Optional


class ServiceBusMessage(BaseModel):
    message_id: str
    sender_email: str
    subject: str
    body: Optional[str] = None
    attachment_base64: Optional[str] = None
    attachment_filename: Optional[str] = None
    received_at: str