from src.services.ticket_service import TicketService
from src.workers.sqs_worker import SQSWorker


def main():
    ticket_service = TicketService()
    worker = SQSWorker()

    ticket_id = ticket_service.create_ticket(
        ticket_text="My order is delayed again and I need help ASAP.",
        user_id="worker_test_user"
    )

    print(f"\nCreated ticket: {ticket_id}")

    result = worker.process_message({"ticket_id": ticket_id})

    print("\nWorker Result:")
    print(result)


if __name__ == "__main__":
    main()