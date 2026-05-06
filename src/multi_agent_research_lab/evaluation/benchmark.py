from time import perf_counter
from typing import Callable, Tuple

from multi_agent_research_lab.core.schemas import BenchmarkMetrics
from multi_agent_research_lab.core.state import ResearchState


Runner = Callable[[str], ResearchState]


def run_benchmark(run_name: str, query: str, runner: Runner) -> Tuple[ResearchState, BenchmarkMetrics]:
    """Measure latency, cost, and citation quality."""

    started = perf_counter()
    state = runner(query)
    latency = perf_counter() - started

    # Calculate citation coverage: unique sources cited in final_answer / total sources found
    citation_coverage = 0.0
    if state.final_answer and state.sources:
        cited_sources = [s for s in state.sources if f"[{s.title}]" in state.final_answer or f"[{s.id}]" in state.final_answer]
        citation_coverage = len(cited_sources) / len(state.sources)

    # Estimate cost (this is usually handled by the LLM client, but we can aggregate here)
    # For now, let's just use a dummy cost if not provided in metadata
    cost = 0.0
    for result in state.agent_results:
        cost += result.metadata.get("cost_usd", 0.0)

    metrics = BenchmarkMetrics(
        run_name=run_name,
        latency_seconds=latency,
        estimated_cost_usd=cost,
        notes=f"Citation coverage: {citation_coverage:.2%}. Errors: {len(state.errors)}"
    )
    
    return state, metrics
