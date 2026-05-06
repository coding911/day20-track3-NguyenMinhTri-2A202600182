from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class SupervisorAgent(BaseAgent):
    """Decides which worker should run next and when to stop."""

    name = "supervisor"

    def __init__(self, llm_client: LLMClient, max_iterations: int = 6):
        self.llm_client = llm_client
        self.max_iterations = max_iterations

    def run(self, state: ResearchState) -> ResearchState:
        """Update `state.route_history` with the next route."""
        
        # Enforce max iterations
        if state.iteration >= self.max_iterations:
            state.record_route("done")
            state.add_trace_event("max_iterations_reached", {"iterations": state.iteration})
            return state

        # Simple deterministic routing for the lab
        if not state.research_notes:
            next_route = "researcher"
        elif not state.analysis_notes:
            next_route = "analyst"
        elif not state.final_answer:
            next_route = "writer"
        elif state.route_history[-1] == "writer":
            next_route = "critic"
        else:
            next_route = "done"

        state.record_route(next_route)
        state.add_trace_event("routed", {"next_agent": next_route})
        return state
