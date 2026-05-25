from langchain_core.tools import tool


@tool
def check_escalation(category: str, ticket_text: str) -> dict:
    """
    Checks if a ticket needs human escalation and determines urgency.
    Use this after a response has been drafted.

    Args:
        category: The classified category of the ticket.
        ticket_text: The original ticket text.
    """
    ticket_lower = ticket_text.lower()

    high_urgency_keywords = [
        "urgent", "immediately", "asap", "critical", "lawsuit",
        "fraud", "angry", "furious", "legal"
    ]

    medium_urgency_keywords = [
        "frustrated", "disappointed", "unacceptable",
        "still not working", "twice", "again"
    ]

    high_score = sum(1 for kw in high_urgency_keywords if kw in ticket_lower)
    medium_score = sum(1 for kw in medium_urgency_keywords if kw in ticket_lower)

    if high_score > 0:
        urgency = "high"
        escalate = True
    elif medium_score > 0:
        urgency = "medium"
        escalate = True
    elif category in ["billing", "technical"]:
        urgency = "medium"
        escalate = False
    else:
        urgency = "low"
        escalate = False

    return {
        "needs_escalation": escalate,
        "urgency_level": urgency,
    }