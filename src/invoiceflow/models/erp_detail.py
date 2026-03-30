from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ERPMatchStatus(str, Enum):
    IDLE = "idle"
    MATCH = "match"
    NO_MATCH = "no_match"


class ERPDetails(BaseModel):
    po_id: Optional[str] = None
    approver: Optional[str] = None
    errors: list[str] = Field(default_factory=list)
    status: ERPMatchStatus = ERPMatchStatus.IDLE