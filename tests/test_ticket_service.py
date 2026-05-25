from src.services.ticket_service import TicketService


def main():
    ticket_service = TicketService()

    ticket_id = ticket_service.create_ticket(
        ticket_text="My order is delayed and I need it urgently.",
        user_id="test_user_001"
    )

    print(f"\nTicket created: {ticket_id}")

    ticket = ticket_service.get_ticket(ticket_id)

    print("\nFetched Ticket:")
    print(ticket)

    ticket_service.update_ticket_state(
        ticket_id=ticket_id,
        ticket_category="delivery",
        draft_response="We are checking your delivery status.",
        needs_escalation=True,
        urgency_level="high",
        status="in_progress",
        agent_state={
            "current_node": "escalation",
            "completed_nodes": ["classifier", "responder"]
        }
    )

    updated_ticket = ticket_service.get_ticket(ticket_id)

    print("\nUpdated Ticket:")
    print(updated_ticket)

    ticket_service.append_message(
        ticket_id=ticket_id,
        role="assistant",
        message="We have escalated this to the delivery team."
    )

    final_ticket = ticket_service.get_ticket(ticket_id)

    print("\nFinal Ticket:")
    print(final_ticket)


if __name__ == "__main__":
    main()