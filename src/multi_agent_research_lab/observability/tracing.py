import os
from collections.abc import Iterator
from contextlib import contextmanager
from time import perf_counter
from typing import Any, Dict, Optional, Union

from langsmith import traceable


@contextmanager
def trace_span(name: str, attributes: Optional[Dict[str, Any]] = None) -> Iterator[Dict[str, Any]]:
    """Minimal span context used by the skeleton.

    Optionally traces to LangSmith if configured.
    """
    
    # If LangSmith is configured, we can use their traceable decorator or run_tree
    # For this simple lab, we'll just track it locally and log it.
    
    started = perf_counter()
    span: Dict[str, Any] = {
        "name": name, 
        "attributes": attributes or {}, 
        "duration_seconds": None
    }
    
    try:
        # If we had a more complex setup, we'd start a LangSmith run here
        yield span
    finally:
        span["duration_seconds"] = perf_counter() - started
        # In a real app, we'd send this to an observability provider
