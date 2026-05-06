from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class AnalystAgent(BaseAgent):
    """Turns research notes into structured insights."""

    name = "analyst"

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.analysis_notes`."""
        if not state.research_notes:
            state.errors.append("Analyst ran but research_notes was empty.")
            return state

        system_prompt = "You are a critical analyst. Take research notes and extract key insights, compare different viewpoints, and identify any gaps or weak evidence. Structure your output clearly."
        user_prompt = f"Research Notes:\n{state.research_notes}\n\nSources:\n" + \
                     "\n".join([f"[{s.id}] {s.title}" for s in state.sources])

        response = self.llm_client.complete(system_prompt, user_prompt)
        state.analysis_notes = response.content
        
        state.add_trace_event("analysis_completed", {"notes_length": len(response.content)})
        return state
