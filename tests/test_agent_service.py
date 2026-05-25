from src.services.ticket_service import TicketService
from src.services.agent_service import AgentService


def main():
    ticket_service = TicketService()
    agent_service = AgentService()

    ticket_id = ticket_service.create_ticket(
        ticket_text="My payment failed but money was deducted. This is urgent.",
        user_id="test_user_agent"
    )

    print(f"\nCreated ticket: {ticket_id}")

    final_ticket = agent_service.process_ticket(ticket_id)

    print("\nFinal Processed Ticket:")
    print(final_ticket)


if __name__ == "__main__":
    main()