from src.graph.builder import build_graph
from src.graph.state_mapper import (
    ticket_to_agent_state,
    agent_state_to_mongo_update,
)
from src.services.ticket_service import TicketService


class AgentService:
    """
    Runs the LangGraph agent workflow for a persisted ticket.
    """

    def __init__(self):
        self.ticket_service = TicketService()
        self.graph = build_graph()

    def process_ticket(self, ticket_id: str) -> dict:
        ticket = self.ticket_service.get_ticket(ticket_id)

        if not ticket:
            raise ValueError(f"Ticket not found: {ticket_id}")

        if ticket.get("status") == "resolved":
            return ticket

        state = ticket_to_agent_state(ticket)

        final_state = self.graph.invoke(state)

        mongo_update = agent_state_to_mongo_update(final_state)

        self.ticket_service.update_ticket_state(
            ticket_id=ticket_id,
            **mongo_update,
        )

        if final_state.get("draft_response"):
            self.ticket_service.append_message(
                ticket_id=ticket_id,
                role="assistant",
                message=final_state["draft_response"],
            )

        return self.ticket_service.get_ticket(ticket_id)