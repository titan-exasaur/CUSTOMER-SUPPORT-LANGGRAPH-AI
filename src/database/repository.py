from typing import Optional
from datetime import datetime, timezone

from src.database.models import Ticket
from src.database.mongo import get_ticket_collection


class TicketRepository:
    """
    Handles all MongoDB operations for support tickets.
    """

    def __init__(self):
        self.collection = get_ticket_collection()
        self.create_indexes()

    def create_indexes(self) -> None:
        """
        Creates indexes for faster lookup and safer uniqueness.
        """
        self.collection.create_index("ticket_id", unique=True)
        self.collection.create_index("user_id")
        self.collection.create_index("status")
        self.collection.create_index("created_at")

    def create_ticket(self, ticket: Ticket) -> str:
        ticket_dict = ticket.to_dict()
        self.collection.insert_one(ticket_dict)
        return ticket.ticket_id

    def get_ticket_by_id(self, ticket_id: str) -> Optional[dict]:
        return self.collection.find_one(
            {"ticket_id": ticket_id},
            {"_id": 0}
        )

    def update_ticket(self, ticket_id: str, update_data: dict) -> bool:
        update_data["updated_at"] = datetime.now(timezone.utc)

        result = self.collection.update_one(
            {"ticket_id": ticket_id},
            {"$set": update_data}
        )

        return result.modified_count > 0

    def append_conversation_message(
        self,
        ticket_id: str,
        role: str,
        message: str
    ) -> bool:
        result = self.collection.update_one(
            {"ticket_id": ticket_id},
            {
                "$push": {
                    "conversation_history": {
                        "role": role,
                        "message": message,
                        "timestamp": datetime.now(timezone.utc)
                    }
                },
                "$set": {
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )

        return result.modified_count > 0

    def mark_resolved(self, ticket_id: str) -> bool:
        ticket = self.get_ticket_by_id(ticket_id)

        if not ticket:
            return False

        resolved_at = datetime.now(timezone.utc)
        created_at = ticket["created_at"]

        resolution_time_seconds = int(
            (resolved_at - created_at).total_seconds()
        )

        result = self.collection.update_one(
            {"ticket_id": ticket_id},
            {
                "$set": {
                    "status": "resolved",
                    "resolved_at": resolved_at,
                    "resolution_time_seconds": resolution_time_seconds,
                    "updated_at": resolved_at
                }
            }
        )

        return result.modified_count > 0

    def log_error(self, ticket_id: str, error_message: str) -> bool:
        result = self.collection.update_one(
            {"ticket_id": ticket_id},
            {
                "$push": {
                    "error_log": {
                        "error": error_message,
                        "timestamp": datetime.now(timezone.utc)
                    }
                },
                "$set": {
                    "updated_at": datetime.now(timezone.utc),
                    "status": "failed"
                }
            }
        )

        return result.modified_count > 0