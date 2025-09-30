# Architecture

## Overview
The project delivers a lightweight retrieval-augmented generation (RAG) toolkit with the following components:

- **Keyword tokeniser & answer stub (`llm_rag.rag_stub`)** — extracts alphanumeric tokens and returns a short stub response.
- **`SimpleIndex` (`llm_rag.index_stub`)** — an in-memory, FAISS-like index using Jaccard similarity with JSON persistence.
- **Pipeline utilities (`llm_rag.pipeline`)** — helpers to build an index from docs and run retrieval + answer.
- **CLI entrypoint (`llm_rag.cli`)** — argparse script that supports loading/saving JSON indices.
- **Gradio integration (`llm_rag.demo_app` & `app/demo_gradio.py`)** — reusable Blocks builders for web demos.

## Data flow
1. Documents (strings or mappings with `text`) are tokenised into sets.
2. `SimpleIndex` stores `(id, text, tokens)` tuples.
3. Queries are tokenised and compared via Jaccard overlap to retrieve top-k docs.
4. `rag_stub.answer` summarises the highest scoring snippet into a stub response.
5. The CLI/Gradio layers orchestrate build/retrieval cycles, optionally using `sample_data/capitals.txt`.

## Persistence
- `SimpleIndex.save(path)` writes a JSON blob (`items`, `next_id`, version field) for portability.
- `SimpleIndex.load(path)` reconstructs the index, re-tokenising stored texts.

## Testing & CI
- Pytest smoke tests cover the index, pipeline, CLI, Gradio demos, Docker config, and documentation.
- GitHub Actions workflow runs `pytest -q` and `ruff check --select=E9,F63,F7,F82 .` on push/PR.
