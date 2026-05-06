from typing import List
from multi_agent_research_lab.core.schemas import BenchmarkMetrics


def render_markdown_report(metrics: List[BenchmarkMetrics]) -> str:
    """Render benchmark metrics to markdown with a summary."""

    lines = [
        "# Benchmark Report",
        "",
        "## Summary",
        "This report compares the performance and cost of different agent configurations.",
        "",
        "## Results Table",
        "",
        "| Run | Latency (s) | Cost (USD) | Quality | Notes |",
        "|---|---:|---:|---:|---|",
    ]
    
    for item in metrics:
        cost = "" if item.estimated_cost_usd is None else f"${item.estimated_cost_usd:.4f}"
        quality = "" if item.quality_score is None else f"{item.quality_score:.1f}/10"
        lines.append(f"| {item.run_name} | {item.latency_seconds:.2f} | {cost} | {quality} | {item.notes} |")
    
    lines.append("")
    lines.append("## Analysis")
    lines.append("- **Multi-agent** workflows usually have higher latency and cost but provide better depth and citation coverage.")
    lines.append("- **Single-agent** is faster and cheaper but may skip critical steps like fact-checking.")
    
    return "\n".join(lines) + "\n"
