from typing import Any, Dict, Literal
from langgraph.graph import StateGraph, END

from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.agents.supervisor import SupervisorAgent
from multi_agent_research_lab.agents.researcher import ResearcherAgent
from multi_agent_research_lab.agents.analyst import AnalystAgent
from multi_agent_research_lab.agents.writer import WriterAgent


from multi_agent_research_lab.agents.critic import CriticAgent


class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph."""

    def __init__(
        self,
        supervisor: SupervisorAgent,
        researcher: ResearcherAgent,
        analyst: AnalystAgent,
        writer: WriterAgent,
        critic: CriticAgent
    ):
        self.supervisor = supervisor
        self.researcher = researcher
        self.analyst = analyst
        self.writer = writer
        self.critic = critic
        self.graph = self.build()

    def build(self) -> Any:
        """Create a LangGraph graph."""
        
        builder = StateGraph(ResearchState)

        # Define nodes
        builder.add_node("supervisor", self.supervisor.run)
        builder.add_node("researcher", self.researcher.run)
        builder.add_node("analyst", self.analyst.run)
        builder.add_node("writer", self.writer.run)
        builder.add_node("critic", self.critic.run)

        # Define edges
        builder.set_entry_point("supervisor")

        def route_condition(state: ResearchState) -> Literal["researcher", "analyst", "writer", "critic", "done"]:
            return state.route_history[-1] if state.route_history else "done"

        builder.add_conditional_edges(
            "supervisor",
            route_condition,
            {
                "researcher": "researcher",
                "analyst": "analyst",
                "writer": "writer",
                "critic": "critic",
                "done": END
            }
        )

        builder.add_edge("researcher", "supervisor")
        builder.add_edge("analyst", "supervisor")
        builder.add_edge("writer", "supervisor")
        builder.add_edge("critic", "supervisor")

        return builder.compile()

    def run(self, state: ResearchState) -> ResearchState:
        """Execute the graph and return final state."""
        return self.graph.invoke(state)
