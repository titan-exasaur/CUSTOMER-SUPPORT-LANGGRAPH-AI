from langchain_core.tools import tool


@tool
def draft_response(category: str, ticket_text: str) -> dict:
    """
    Drafts an initial response template based on the ticket category.
    Use this after the ticket has been classified.

    Args:
        category: The classified category.
        ticket_text: The original ticket text.
    """
    templates = {
        "billing": (
            "Thank you for reaching out about your billing concern. "
            "I can see this is regarding a payment issue, and I want to make this right for you. "
            "Our billing team will review your account and get back to you shortly."
        ),
        "technical": (
            "Thank you for reporting this technical issue. "
            "I understand how frustrating this must be. "
            "Our technical team has been notified and will investigate the issue."
        ),
        "delivery": (
            "Thank you for contacting us about your delivery issue. "
            "We understand how important timely delivery is. "
            "Our support team will review the shipment details and update you soon."
        ),
        "general": (
            "Thank you for contacting our support team. "
            "We have received your inquiry and will get back to you within 1 business day."
        ),
    }

    return {
        "draft": templates.get(category, templates["general"]),
        "category_used": category,
    }