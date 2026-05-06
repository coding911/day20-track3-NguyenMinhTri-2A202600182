# Design Document - Multi-Agent Research System

## Problem

Building a research assistant that can handle complex queries, synthesize information from multiple sources, fact-check its own work, and provide a polished final answer.

## Why multi-agent?

A single-agent approach often struggles with:
- **Depth**: It may skip detailed research or analysis.
- **Accuracy**: It lacks a dedicated fact-checking step (hallucination risk).
- **Structure**: It may produce disorganized outputs for complex topics.
- **Reliability**: It doesn't have explicit handoffs or self-correction loops.

## Agent roles

| Agent | Responsibility | Input | Output | Failure mode |
|---|---|---|---|---|
| Supervisor | Orchestrates the workflow and decides next steps. | Shared State | Next Agent Name | Infinite loops, incorrect routing. |
| Researcher | Finds information and summarizes search results. | Query | Research Notes, Sources | Irrelevant sources, poor summarization. |
| Analyst | Synthesizes notes into critical insights. | Research Notes | Analysis Notes | Misinterpreting data, missing key points. |
| Writer | Crafts the final comprehensive response. | Analysis & Research Notes | Final Answer | Inconsistent tone, losing source context. |
| Critic | Fact-checks and validates citations. | Final Answer, Sources | Validation Result | Overly harsh or missing subtle errors. |

## Shared State

The `ResearchState` (Pydantic model) contains:
- `request`: Original query and config.
- `sources`: List of documents found.
- `research_notes`: Summarized info.
- `analysis_notes`: Critically analyzed info.
- `final_answer`: The end product.
- `route_history`: Track of agent execution.
- `trace`: Event log for debugging.

## Routing Policy

The graph follows a linear-but-conditional path:
`Supervisor` -> `Researcher` -> `Analyst` -> `Writer` -> `Critic` -> `Done` (or loop back if errors detected).

## Guardrails

- **Max iterations**: 6 (prevent infinite loops).
- **Timeout**: 60 seconds.
- **Retry**: Exponential backoff (3 attempts) for LLM calls.
- **Validation**: Critic agent verifies final output before completion.

## Benchmark Plan

- **Queries**: Complex technical topics (e.g., "GraphRAG state-of-the-art").
- **Metrics**: Latency (s), Token Cost ($), Citation Coverage (%), Quality (0-10).
- **Expected Outcome**: Multi-agent should have higher quality/citation coverage but higher latency/cost.
