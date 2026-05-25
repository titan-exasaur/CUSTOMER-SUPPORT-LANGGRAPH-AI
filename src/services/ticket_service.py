import uuid
from typing import Optional

from src.config.settings import settings
from src.database.models import Ticket
from src.database.repository import TicketRepository


class TicketService:
    """
    Business logic layer for ticket operations.
    """

    def __init__(self):
        self.repository = TicketRepository()

    def create_ticket(
        self,
        ticket_text: str,
        user_id: str = "anonymous"
    ) -> str:
        ticket_id = str(uuid.uuid4())

        ticket = Ticket(
            ticket_id=ticket_id,
            user_id=user_id,
            ticket_text=ticket_text,
            model_name=settings.MODEL_NAME
        )

        self.repository.create_ticket(ticket)

        self.repository.append_conversation_message(
            ticket_id=ticket_id,
            role="user",
            message=ticket_text
        )

        return ticket_id

    def get_ticket(self, ticket_id: str) -> Optional[dict]:
        return self.repository.get_ticket_by_id(ticket_id)

    def update_ticket_state(
        self,
        ticket_id: str,
        ticket_category: Optional[str] = None,
        draft_response: Optional[str] = None,
        needs_escalation: Optional[bool] = None,
        urgency_level: Optional[str] = None,
        status: Optional[str] = None,
        agent_state: Optional[dict] = None,
        token_usage: Optional[dict] = None
    ) -> bool:
        update_data = {}

        if ticket_category is not None:
            update_data["ticket_category"] = ticket_category

        if draft_response is not None:
            update_data["draft_response"] = draft_response

        if needs_escalation is not None:
            update_data["needs_escalation"] = needs_escalation

        if urgency_level is not None:
            update_data["urgency_level"] = urgency_level

        if status is not None:
            update_data["status"] = status

        if agent_state is not None:
            update_data["agent_state"] = agent_state

        if token_usage is not None:
            update_data["token_usage"] = token_usage

        if not update_data:
            return False

        return self.repository.update_ticket(ticket_id, update_data)

    def append_message(
        self,
        ticket_id: str,
        role: str,
        message: str
    ) -> bool:
        return self.repository.append_conversation_message(
            ticket_id=ticket_id,
            role=role,
            message=message
        )

    def mark_ticket_resolved(self, ticket_id: str) -> bool:
        return self.repository.mark_resolved(ticket_id)

    def mark_ticket_failed(self, ticket_id: str, error_message: str) -> bool:
        return self.repository.log_error(ticket_id, error_message)