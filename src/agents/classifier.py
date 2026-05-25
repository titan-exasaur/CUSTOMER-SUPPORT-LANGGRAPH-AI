import json

from langchain_core.messages import SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI

from src.config.settings import settings
from src.graph.state import AgentState
from src.tools.classify_ticket import classify_ticket


llm = ChatOpenAI(
    model=settings.MODEL_NAME,
    temperature=settings.TEMPERATURE
)

classifier_llm = llm.bind_tools([classify_ticket])


def classifier_agent(state: AgentState) -> dict:
    print("\n[Classifier] Running...")

    messages = [
        SystemMessage(
            content=(
                "You are a ticket classifier. "
                "You MUST always use the classify_ticket tool for every ticket. "
                "Do not respond with text. Only call the tool."
            )
        )
    ] + state["messages"]

    response = classifier_llm.invoke(messages)

    if not response.tool_calls:
        print("[Classifier] LLM skipped tool. Defaulting to general.")

        return {
            "messages": [response],
            "ticket_category": "general",
            "current_node": "classifier",
            "completed_nodes": state.get("completed_nodes", []) + ["classifier"],
        }

    tool_call = response.tool_calls[0]
    result = classify_ticket.invoke(tool_call["args"])

    print(f"[Classifier] Category: {result['category']}")

    return {
        "messages": [
            response,
            ToolMessage(
                content=json.dumps(result),
                tool_call_id=tool_call["id"]
            )
        ],
        "ticket_category": result["category"],
        "current_node": "classifier",
        "completed_nodes": state.get("completed_nodes", []) + ["classifier"],
    }