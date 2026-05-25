from typing import Optional
from pydantic import BaseModel, Field


class TicketCreateRequest(BaseModel):
    user_id: str = Field(default="anonymous")
    ticket_text: str = Field(..., min_length=1)


class TicketCreateResponse(BaseModel):
    ticket_id: str
    status: str
    message: str


class TicketStatusResponse(BaseModel):
    ticket_id: str
    user_id: str
    ticket_text: str
    ticket_category: Optional[str] = None
    draft_response: Optional[str] = None
    needs_escalation: Optional[bool] = None
    urgency_level: Optional[str] = None
    status: str