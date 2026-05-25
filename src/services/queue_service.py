class QueueService:
    """
    Queue abstraction layer.
    Local mode prints ticket_id.
    AWS mode will push ticket_id to SQS.
    """

    def send_ticket_for_processing(self, ticket_id: str) -> bool:
        print(f"[QueueService] Ticket queued for processing: {ticket_id}")
        return True