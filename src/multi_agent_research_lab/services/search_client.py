import os
import requests
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.schemas import SourceDocument


class SearchClient:
    """Provider-agnostic search client skeleton."""

    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")

    def search(self, query: str, max_results: int = 5) -> list[SourceDocument]:
        """Search for documents relevant to a query.

        Uses Tavily API if available, otherwise returns mock results.
        """
        if not self.api_key:
            # Fallback to mock results for lab purposes if no key is provided
            return [
                SourceDocument(
                    id="mock-1",
                    title=f"Mock result for {query}",
                    content=f"This is a mock research result for the query: {query}. In a real scenario, this would contain scraped content from the web.",
                    url="https://example.com/mock-1",
                    metadata={"source": "mock"}
                )
            ]

        try:
            response = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": self.api_key,
                    "query": query,
                    "search_depth": "smart",
                    "max_results": max_results
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            results = []
            for i, res in enumerate(data.get("results", [])):
                results.append(SourceDocument(
                    id=f"tavily-{i}",
                    title=res.get("title", "No Title"),
                    content=res.get("content", ""),
                    url=res.get("url", ""),
                    metadata={"score": res.get("score", 0)}
                ))
            return results
        except Exception as e:
            # Fallback to mock on error
            return [
                SourceDocument(
                    id="error-fallback",
                    title="Search Error Fallback",
                    content=f"Search failed with error: {str(e)}. Returning fallback content.",
                    url="https://example.com/error",
                    metadata={"error": True}
                )
            ]
