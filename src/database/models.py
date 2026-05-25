from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Ticket:
    ticket_id: str
    user_id: str
    ticket_text: str
    agent_state: dict = field(default_factory=dict)
    ticket_category: Optional[str] = None
    draft_response: Optional[str] = None
    needs_escalation: Optional[bool] = None
    urgency_level: Optional[str] = None

    status: str = "open"

    conversation_history: list = field(default_factory=list)

    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    resolved_at: Optional[datetime] = None
    resolution_time_seconds: Optional[int] = None

    error_log: list = field(default_factory=list)

    model_name: str = "gpt-4o-mini"

    token_usage: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """
        Converts Ticket object into MongoDB-compatible dictionary.
        """
        return asdict(self)