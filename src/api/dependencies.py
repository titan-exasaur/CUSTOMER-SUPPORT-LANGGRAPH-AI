from src.services.ticket_service import TicketService
from src.services.queue_service import QueueService
from src.services.agent_service import AgentService


def get_ticket_service() -> TicketService:
    return TicketService()

def get_queue_service() -> QueueService:
    return QueueService()

def get_agent_service() -> AgentService:
    return AgentService()