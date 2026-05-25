import json

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI

from src.config.settings import settings
from src.graph.state import AgentState
from src.tools.check_escalation import check_escalation


llm = ChatOpenAI(
    model=settings.MODEL_NAME,
    temperature=settings.TEMPERATURE
)

escalation_llm = llm.bind_tools([check_escalation])


def escalation_agent(state: AgentState) -> dict:
    print("\n[Escalation] Running...")

    category = state["ticket_category"]
    ticket_text = state["ticket_text"]

    messages = [
        SystemMessage(
            content=(
                f"You are an escalation checker. "
                f"The ticket category is: {category}. "
                f"You MUST use the check_escalation tool to determine whether "
                f"the ticket needs human review. "
                f"Do not respond with text. Only call the tool."
            )
        ),
        HumanMessage(content=ticket_text),
    ]

    response = escalation_llm.invoke(messages)

    if not response.tool_calls:
        print("[Escalation] LLM skipped tool. Defaulting to no escalation.")

        return {
            "messages": [response],
            "needs_escalation": False,
            "urgency_level": "low",
            "status": "resolved",
            "current_node": "escalation",
            "completed_nodes": state.get("completed_nodes", []) + ["escalation"],
        }

    tool_call = response.tool_calls[0]
    result = check_escalation.invoke(tool_call["args"])

    print(
        f"[Escalation] Needs escalation: {result['needs_escalation']} | "
        f"Urgency: {result['urgency_level']}"
    )

    status = "escalated" if result["needs_escalation"] else "resolved"

    return {
        "messages": [
            response,
            ToolMessage(
                content=json.dumps(result),
                tool_call_id=tool_call["id"]
            )
        ],
        "needs_escalation": result["needs_escalation"],
        "urgency_level": result["urgency_level"],
        "status": status,
        "current_node": "escalation",
        "completed_nodes": state.get("completed_nodes", []) + ["escalation"],
    }