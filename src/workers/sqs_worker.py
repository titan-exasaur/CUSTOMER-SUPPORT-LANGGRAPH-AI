from src.services.agent_service import AgentService

class SQSWorker:
    """
    Local simulation of an AWS SQS worker.
    Later this file will become the Lambda worker entry point.
    """

    def __init__(self):
        self.agent_service = AgentService()

    def process_message(self, message: dict) -> dict:
        ticket_id = message.get("ticket_id")

        if not ticket_id:
            raise ValueError("ticket_id missing from queue message")

        print(f"[SQSWorker] Processing ticket: {ticket_id}")

        final_ticket = self.agent_service.process_ticket(ticket_id)

        print(f"[SQSWorker] Finished ticket: {ticket_id}")

        return final_ticket