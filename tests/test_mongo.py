import uuid

from src.database.models import Ticket
from src.database.repository import TicketRepository


def main():
    repository = TicketRepository()

    ticket_id = str(uuid.uuid4())

    # Create ticket
    ticket = Ticket(
        ticket_id=ticket_id,
        user_id="test_user",
        ticket_text="My payment failed but money was deducted."
    )

    repository.create_ticket(ticket)

    print("\nTicket inserted successfully.\n")

    # Retrieve ticket
    retrieved_ticket = repository.get_ticket_by_id(ticket_id)

    print("Retrieved Ticket:\n")
    print(retrieved_ticket)

    # Update ticket
    repository.update_ticket(
        ticket_id=ticket_id,
        update_data={
            "ticket_category": "billing",
            "urgency_level": "high"
        }
    )

    print("\nTicket updated successfully.\n")

    # Append conversation
    repository.append_conversation_message(
        ticket_id=ticket_id,
        role="assistant",
        message="We are checking your billing issue."
    )

    print("\nConversation updated successfully.\n")

    # Fetch final state
    final_ticket = repository.get_ticket_by_id(ticket_id)

    print("\nFinal Ticket State:\n")
    print(final_ticket)


if __name__ == "__main__":
    main()