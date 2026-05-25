from langchain_core.messages import HumanMessage, AIMessage

from src.graph.state import AgentState


def ticket_to_agent_state(ticket: dict) -> AgentState:
    """
    Converts Mongo ticket document into LangGraph AgentState.
    """

    messages = []

    for item in ticket.get("conversation_history", []):
        role = item.get("role")
        message = item.get("message")

        if role == "user":
            messages.append(HumanMessage(content=message))
        elif role == "assistant":
            messages.append(AIMessage(content=message))

    return AgentState(
        messages=messages,
        ticket_id=ticket["ticket_id"],
        user_id=ticket["user_id"],
        status=ticket.get("status", "open"),
        ticket_text=ticket["ticket_text"],
        ticket_category=ticket.get("ticket_category"),
        draft_response=ticket.get("draft_response"),
        needs_escalation=ticket.get("needs_escalation"),
        urgency_level=ticket.get("urgency_level"),
        current_node=ticket.get("agent_state", {}).get("current_node"),
        completed_nodes=ticket.get("agent_state", {}).get("completed_nodes", []),
    )


def agent_state_to_mongo_update(state: AgentState) -> dict:
    """
    Converts LangGraph AgentState into Mongo update payload.
    """

    return {
        "ticket_category": state.get("ticket_category"),
        "draft_response": state.get("draft_response"),
        "needs_escalation": state.get("needs_escalation"),
        "urgency_level": state.get("urgency_level"),
        "status": state.get("status"),
        "agent_state": {
            "current_node": state.get("current_node"),
            "completed_nodes": state.get("completed_nodes", []),
        },
    }