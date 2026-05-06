import typer
from typing import Annotated
from rich.console import Console
from rich.panel import Panel

from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow
from multi_agent_research_lab.observability.logging import configure_logging
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.services.search_client import SearchClient
from multi_agent_research_lab.agents.supervisor import SupervisorAgent
from multi_agent_research_lab.agents.researcher import ResearcherAgent
from multi_agent_research_lab.agents.analyst import AnalystAgent
from multi_agent_research_lab.agents.writer import WriterAgent

from multi_agent_research_lab.agents.critic import CriticAgent

app = typer.Typer(help="Multi-Agent Research Lab starter CLI")
console = Console()


def _init() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)


@app.command()
def baseline(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run a single-agent baseline implementation."""

    _init()
    llm_client = LLMClient()
    request = ResearchQuery(query=query)
    state = ResearchState(request=request)
    
    system_prompt = "You are a research assistant. Provide a comprehensive answer to the user's query."
    response = llm_client.complete(system_prompt, query)
    
    state.final_answer = response.content
    console.print(Panel(state.final_answer, title="Single-Agent Baseline"))
    console.print(f"\n[bold]Cost:[/bold] ${response.cost_usd:.4f}")
    console.print(f"[bold]Tokens:[/bold] {response.input_tokens + response.output_tokens}")


@app.command("multi-agent")
def multi_agent(
    query: Annotated[str, typer.Option("--query", "-q", help="Research query")],
) -> None:
    """Run the multi-agent workflow."""

    _init()
    llm_client = LLMClient()
    search_client = SearchClient()
    
    supervisor = SupervisorAgent(llm_client=llm_client)
    researcher = ResearcherAgent(llm_client=llm_client, search_client=search_client)
    analyst = AnalystAgent(llm_client=llm_client)
    writer = WriterAgent(llm_client=llm_client)
    critic = CriticAgent(llm_client=llm_client)
    
    workflow = MultiAgentWorkflow(
        supervisor=supervisor,
        researcher=researcher,
        analyst=analyst,
        writer=writer,
        critic=critic
    )
    
    state = ResearchState(request=ResearchQuery(query=query))
    
    try:
        with console.status("[bold green]Running multi-agent workflow..."):
            raw_result = workflow.run(state)
            # LangGraph often returns a dict even if StateGraph was initialized with a model
            if isinstance(raw_result, dict):
                result = ResearchState(**raw_result)
            else:
                result = raw_result
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1) from e
        
    console.print(Panel(result.final_answer or "No answer generated.", title="Multi-Agent Result"))
    console.print(f"\n[bold]History:[/bold] {' -> '.join(result.route_history)}")
    console.print(f"[bold]Sources:[/bold] {len(result.sources)}")


if __name__ == "__main__":
    app()
