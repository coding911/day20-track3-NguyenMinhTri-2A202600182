from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class WriterAgent(BaseAgent):
    """Produces final answer from research and analysis notes."""

    name = "writer"

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.final_answer`."""
        if not state.analysis_notes:
            state.errors.append("Writer ran but analysis_notes was empty.")
            return state

        system_prompt = "You are a professional writer. Synthesize the research and analysis notes into a final, polished answer that directly addresses the user's query. Include citations where appropriate using [Source Title] or [id]."
        user_prompt = f"Original Query: {state.request.query}\n\nResearch Notes:\n{state.research_notes}\n\nAnalysis Notes:\n{state.analysis_notes}"

        response = self.llm_client.complete(system_prompt, user_prompt)
        state.final_answer = response.content
        
        state.add_trace_event("writing_completed", {"answer_length": len(response.content)})
        return state
