import json
from typing import Optional

import boto3

from src.config.settings import settings


class QueueService:
    """
    Queue abstraction layer.

    Local mode:
        Prints the ticket_id.

    AWS mode:
        Sends ticket_id to SQS.
    """

    def __init__(self):
        self.queue_url: Optional[str] = settings.SQS_QUEUE_URL

        if self.queue_url:
            self.sqs_client = boto3.client(
                "sqs",
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
        else:
            self.sqs_client = None

    def send_ticket_for_processing(self, ticket_id: str) -> bool:
        message_body = {
            "ticket_id": ticket_id
        }

        if not self.sqs_client or not self.queue_url:
            print(f"[QueueService:LOCAL] Ticket queued: {ticket_id}")
            return True

        self.sqs_client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(message_body)
        )

        print(f"[QueueService:AWS] Ticket sent to SQS: {ticket_id}")
        return True