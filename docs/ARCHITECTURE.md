# Architecture & Design

This project packages a compact RAG stack and automation demos that run entirely offline.

## High-level flow
```mermaid
flowchart LR
  Q[User query] --> R[SimpleIndex.search (Jaccard)]
  R --> K[Top-K documents]
  K --> A[rag_stub.answer (stub)]
  A --> O[Answer]
```

## Modules
- `rag_stub.answer(query, docs)` – returns a stubbed response derived from the best-matching document.
- `index_stub.SimpleIndex` – in-memory index with `add_many`, `search`, and JSON serialisation (`save`/`load`). Stable ordering ensures deterministic tests.
- `pipeline` – `build_index(docs)` and `rag_pipeline(query, index|docs, k)` for reusable orchestration.
- `docqa` – loads TXT (one document per line) and, if available, PDF snippets via `pypdf`; otherwise falls back to sample TXT.
- `chatbot` – rule-based intents (ticket creation, meeting scheduling) with RAG fallback for other prompts.
- `resume` – keyword skill extraction, scoring, and ranking (TXT by default; PDF optional).
- `reporting` – generates a Markdown daily report, ≤280-character social post, SVG card, and JSON scheduling entry.

## Data considerations
- Synthetic corpora only (`sample_data/`): capitals, generated PDFs, SVG card, scheduling JSON.
- No secrets; environment variables configure demo behaviour (host/port) rather than credentials.

## Design choices
- **Minimal dependencies** favour portability and clarity.
- **Deterministic behaviour** (stable sorting, simple heuristics) keeps tests predictable.
- **Extensibility** – modules are importable and can seed other demonstrations or tutorials.
