import json
from src.workers.sqs_worker import SQSWorker

worker = SQSWorker()

def handler(event, context):
    """
    AWS Lambda entry point for SQS-triggered ticket processing.
    """

    results = []

    for record in event.get("Records", []):
        body = json.loads(record["body"])
        ticket_id = body.get("ticket_id")

        if not ticket_id:
            results.append({"status": "skipped", "reason": "missing ticket_id"})
            continue

        final_ticket = worker.process_message({"ticket_id": ticket_id})

        results.append({
            "ticket_id": ticket_id,
            "status": final_ticket.get("status"),
        })

    return {
        "statusCode": 200,
        "body": json.dumps(results),
    }