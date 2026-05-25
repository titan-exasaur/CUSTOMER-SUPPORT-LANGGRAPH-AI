from src.services.ticket_service import TicketService
from src.services.agent_service import AgentService


def main():
    ticket_text = input("\nEnter customer complaint: ").strip()

    if not ticket_text:
        print("Ticket text cannot be empty.")
        return

    ticket_service = TicketService()
    agent_service = AgentService()

    ticket_id = ticket_service.create_ticket(
        ticket_text=ticket_text,
        user_id="local_user"
    )

    print(f"\nTicket created: {ticket_id}")

    final_ticket = agent_service.process_ticket(ticket_id)

    print("\nFinal Ticket Result:")
    print(f"Ticket ID: {final_ticket['ticket_id']}")
    print(f"Category: {final_ticket['ticket_category']}")
    print(f"Urgency: {final_ticket['urgency_level']}")
    print(f"Escalation Needed: {final_ticket['needs_escalation']}")
    print(f"Status: {final_ticket['status']}")
    print(f"Draft Response: {final_ticket['draft_response']}")


if __name__ == "__main__":
    main()