from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    TicketCreateRequest,
    TicketCreateResponse,
    TicketStatusResponse,
)
from src.services.ticket_service import TicketService
from src.services.agent_service import AgentService


router = APIRouter()

ticket_service = TicketService()
agent_service = AgentService()


@router.post("/tickets", response_model=TicketCreateResponse)
def create_ticket(request: TicketCreateRequest):
    ticket_id = ticket_service.create_ticket(
        ticket_text=request.ticket_text,
        user_id=request.user_id,
    )

    # Current local mode: process immediately.
    # Later AWS v2 mode: push ticket_id to SQS instead.
    agent_service.process_ticket(ticket_id)

    return TicketCreateResponse(
        ticket_id=ticket_id,
        status="processing",
        message="Ticket created successfully.",
    )


@router.get("/tickets/{ticket_id}", response_model=TicketStatusResponse)
def get_ticket_status(ticket_id: str):
    ticket = ticket_service.get_ticket(ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return TicketStatusResponse(**ticket)