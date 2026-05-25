import json

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI

from src.config.settings import settings
from src.graph.state import AgentState
from src.tools.draft_response import draft_response


llm = ChatOpenAI(
    model=settings.MODEL_NAME,
    temperature=settings.TEMPERATURE
)

responder_llm = llm.bind_tools([draft_response])


def responder_agent(state: AgentState) -> dict:
    print("\n[Responder] Running...")

    category = state["ticket_category"]
    ticket_text = state["ticket_text"]

    messages = [
        SystemMessage(
            content=(
                f"You are a customer support responder. "
                f"The ticket has been classified as: {category}. "
                f"You MUST use the draft_response tool to draft a reply. "
                f"Do not respond with text. Only call the tool."
            )
        ),
        HumanMessage(content=ticket_text),
    ]

    response = responder_llm.invoke(messages)

    if not response.tool_calls:
        print("[Responder] LLM skipped tool. Defaulting to generic response.")

        fallback_response = (
            "Thank you for contacting our support team. "
            "We have received your inquiry and will get back to you shortly."
        )

        return {
            "messages": [response],
            "draft_response": fallback_response,
            "current_node": "responder",
            "completed_nodes": state.get("completed_nodes", []) + ["responder"],
        }

    tool_call = response.tool_calls[0]
    result = draft_response.invoke(tool_call["args"])

    print(f"[Responder] Draft: {result['draft'][:60]}...")

    return {
        "messages": [
            response,
            ToolMessage(
                content=json.dumps(result),
                tool_call_id=tool_call["id"]
            )
        ],
        "draft_response": result["draft"],
        "current_node": "responder",
        "completed_nodes": state.get("completed_nodes", []) + ["responder"],
    }