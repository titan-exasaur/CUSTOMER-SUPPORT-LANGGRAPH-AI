from langchain_core.tools import tool


@tool
def classify_ticket(ticket_text: str) -> dict:
    """
    Classifies a customer support ticket into a category.
    Use this when you receive a support ticket.

    Args:
        ticket_text: The raw text of the customer support ticket.
    """
    ticket_lower = ticket_text.lower()

    billing_keywords = [
        "invoice", "charge", "payment", "refund", "billing", "subscription", "money"
    ]

    technical_keywords = [
        "error", "crash", "bug", "not working", "login", "password", "404"
    ]

    delivery_keywords = [
        "delivery", "order", "shipment", "delayed", "late", "tracking"
    ]

    billing_score = sum(1 for kw in billing_keywords if kw in ticket_lower)
    technical_score = sum(1 for kw in technical_keywords if kw in ticket_lower)
    delivery_score = sum(1 for kw in delivery_keywords if kw in ticket_lower)

    scores = {
        "billing": billing_score,
        "technical": technical_score,
        "delivery": delivery_score,
    }

    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        best_category = "general"

    return {"category": best_category}