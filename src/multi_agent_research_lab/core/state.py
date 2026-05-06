from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from multi_agent_research_lab.core.schemas import AgentResult, ResearchQuery, SourceDocument


class ResearchState(BaseModel):
    """Single source of truth passed through the workflow."""

    request: ResearchQuery
    iteration: int = 0
    route_history: List[str] = Field(default_factory=list)

    sources: List[SourceDocument] = Field(default_factory=list)
    research_notes: Optional[str] = None
    analysis_notes: Optional[str] = None
    final_answer: Optional[str] = None

    agent_results: List[AgentResult] = Field(default_factory=list)
    trace: List[Dict[str, Any]] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)

    def record_route(self, route: str) -> None:
        self.route_history.append(route)
        self.iteration += 1

    def add_trace_event(self, name: str, payload: Dict[str, Any]) -> None:
        self.trace.append({"name": name, "payload": payload})
