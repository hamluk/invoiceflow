from pydantic import BaseModel
from typing import Optional


class ServiceBusMessage(BaseModel):
    invoice_content: Optional[str] = None
    image_b64encoded: Optional[str] = None
    received_at: str
    is_scan: bool
