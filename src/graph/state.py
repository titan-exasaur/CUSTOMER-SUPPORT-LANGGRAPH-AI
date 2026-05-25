from typing import Annotated, List, Optional, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    # LangGraph conversation memory
    messages: Annotated[List[BaseMessage], add_messages]

    # Mongo tracking
    ticket_id: str
    user_id: str
    status: str

    # Input
    ticket_text: str

    # Agent outputs
    ticket_category: Optional[str]
    draft_response: Optional[str]
    needs_escalation: Optional[bool]
    urgency_level: Optional[str]

    # Resume/debug metadata
    current_node: Optional[str]
    completed_nodes: List[str]