from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class CriticAgent(BaseAgent):
    """Optional fact-checking and safety-review agent."""

    name = "critic"

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def run(self, state: ResearchState) -> ResearchState:
        """Validate final answer and append findings."""
        if not state.final_answer:
            state.errors.append("Critic ran but final_answer was empty.")
            return state

        system_prompt = (
            "You are a rigorous fact-checker. Review the provided answer against the research notes and sources. "
            "Check for hallucinations, incorrect citations, or unsupported claims. "
            "If the answer is good, say 'PASSED'. If it needs changes, specify what is wrong."
        )
        user_prompt = (
            f"Research Notes:\n{state.research_notes}\n\n"
            f"Sources:\n" + "\n".join([f"[{s.id}] {s.title}" for s in state.sources]) + "\n\n"
            f"Answer to Review:\n{state.final_answer}"
        )

        response = self.llm_client.complete(system_prompt, user_prompt)
        
        # We'll store the critique in metadata or a new field if we want
        # For now, let's just record a trace event
        state.add_trace_event("critique_completed", {"result": response.content})
        
        if "PASSED" not in response.content.upper():
            state.errors.append(f"Critique failed: {response.content[:100]}...")
            
        return state
