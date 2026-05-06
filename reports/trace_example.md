# Multi-Agent Execution Trace Example

This trace shows the internal execution log of the multi-agent system for the query: *"Research GraphRAG state-of-the-art"*.

## Workflow History
`supervisor` -> `researcher` -> `supervisor` -> `analyst` -> `supervisor` -> `writer` -> `supervisor` -> `critic` -> `supervisor` -> `done`

## Detailed Step Logs (Simplified)

### 1. Supervisor (Entry)
- **Action**: Routing to `researcher`
- **Reason**: No research notes found in state.

### 2. Researcher
- **Action**: Searching for "GraphRAG state-of-the-art"
- **Result**: Found 1 mock source.
- **Output**: Summarized research notes with citations.

### 3. Analyst
- **Action**: Analyzing research notes.
- **Output**: Identified key themes: Integration of Knowledge Graphs, Retrieval Augmentation, and hallucination reduction.

### 4. Writer
- **Action**: Writing final response.
- **Output**: 300-word summary with structured sections and citations.

### 5. Critic
- **Action**: Fact-checking the answer.
- **Result**: `PASSED`. The answer correctly reflects the research notes and cites sources properly.

### 6. Supervisor (Exit)
- **Action**: Routing to `done`
- **Reason**: All stages completed successfully.

---
**Total Tokens**: ~2,500
**Total Latency**: 42.5s
**Total Cost**: $0.0018
