from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import date


class InvoiceStatus(str, Enum):
    ARRIVED = "arrived"
    EXTRACTED = "extracted"
    VALIDATED = "validated"
    MANUAL_REVIEW = "manual_review"
    FAILED = "failed"


class ValidationStatus(BaseModel):
    status: InvoiceStatus = InvoiceStatus.ARRIVED
    validation_errors: list[str] = Field(default_factory=list)


class InvoiceLineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    vat_rate: float
    amount_net: float


class Invoice(BaseModel):
    supplier_name: str
    supplier_uid: str
    recipient_mandant_id: str

    invoice_number: str
    invoice_date: date

    po_number: Optional[str] = None

    line_items: list[InvoiceLineItem]
    amount_net: float
    amount_vat_10: float
    amount_vat_20: float
    amount_gross: float

    iban: str
    amount_due_in: str

    llm_detected_errors: list[str] = Field(default_factory=list)
    validation_status: ValidationStatus
