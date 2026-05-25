from src.services.ticket_service import TicketService
from src.services.agent_service import AgentService


def get_ticket_service() -> TicketService:
    return TicketService()


def get_agent_service() -> AgentService:
    return AgentService()