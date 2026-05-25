from fastapi import APIRouter, Depends, HTTPException

from src.api.schemas import (
    TicketCreateRequest,
    TicketCreateResponse,
    TicketStatusResponse,
)
from src.api.dependencies import (
    get_ticket_service,
    get_queue_service,
    get_agent_service,
)
from src.services.ticket_service import TicketService
from src.services.queue_service import QueueService
from src.services.agent_service import AgentService


router = APIRouter()


@router.post("/tickets", response_model=TicketCreateResponse)
def create_ticket(
    request: TicketCreateRequest,
    ticket_service: TicketService = Depends(get_ticket_service),
    queue_service: QueueService = Depends(get_queue_service),
):
    ticket_id = ticket_service.create_ticket(
        ticket_text=request.ticket_text,
        user_id=request.user_id,
    )

    queue_service.send_ticket_for_processing(ticket_id)

    return TicketCreateResponse(
        ticket_id=ticket_id,
        status="queued",
        message="Ticket created and queued for processing.",
    )


@router.get("/tickets/{ticket_id}", response_model=TicketStatusResponse)
def get_ticket_status(
    ticket_id: str,
    ticket_service: TicketService = Depends(get_ticket_service),
):
    ticket = ticket_service.get_ticket(ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return TicketStatusResponse(**ticket)


@router.post("/tickets/{ticket_id}/process", response_model=TicketStatusResponse)
def process_ticket_locally(
    ticket_id: str,
    agent_service: AgentService = Depends(get_agent_service),
):
    """
    Local/dev-only endpoint to simulate SQS worker processing.
    In AWS, SQS will trigger the worker Lambda instead.
    """
    try:
        ticket = agent_service.process_ticket(ticket_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return TicketStatusResponse(**ticket)