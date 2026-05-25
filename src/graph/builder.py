from langgraph.graph import StateGraph, END

from src.graph.state import AgentState
from src.agents.classifier import classifier_agent
from src.agents.responder import responder_agent
from src.agents.escalation import escalation_agent


def build_graph():
    """
    Builds and compiles the customer support triage LangGraph workflow.
    """

    graph = StateGraph(AgentState)

    graph.add_node("classifier", classifier_agent)
    graph.add_node("responder", responder_agent)
    graph.add_node("escalation", escalation_agent)

    graph.set_entry_point("classifier")

    graph.add_edge("classifier", "responder")
    graph.add_edge("responder", "escalation")
    graph.add_edge("escalation", END)

    return graph.compile()