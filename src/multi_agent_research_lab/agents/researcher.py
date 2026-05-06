from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.services.search_client import SearchClient


class ResearcherAgent(BaseAgent):
    """Collects sources and creates concise research notes."""

    name = "researcher"

    def __init__(self, llm_client: LLMClient, search_client: SearchClient):
        self.llm_client = llm_client
        self.search_client = search_client

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.sources` and `state.research_notes`."""
        query = state.request.query
        
        # 1. Search for sources
        sources = self.search_client.search(query)
        state.sources.extend(sources)

        # 2. Synthesize research notes
        source_text = "\n\n".join([f"Source [{s.id}] ({s.title}): {s.content}" for s in sources])
        system_prompt = "You are a world-class researcher. Summarize the provided search results into concise, factual research notes. Use citations like [id]."
        user_prompt = f"Research Query: {query}\n\nSearch Results:\n{source_text}"

        response = self.llm_client.complete(system_prompt, user_prompt)
        state.research_notes = response.content
        
        state.add_trace_event("research_completed", {"num_sources": len(sources)})
        return state
