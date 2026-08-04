# RAGworks

[![CI](https://img.shields.io/github/actions/workflow/status/M2002HR/RAGworks/ci.yml?branch=master&label=CI)](https://github.com/M2002HR/RAGworks/actions)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)

**An offline AI-application portfolio with lightweight retrieval, document Q&A, workflow demos, Docker services, tests, and CI.**

RAGworks packages several small, self-contained examples behind reusable Python modules, CLI commands, and Gradio interfaces. It is intentionally dependency-light and runs on synthetic/local data without external model APIs.

> The retrieval layer is a transparent keyword/Jaccard implementation for demonstration and testing. It is not presented as semantic vector search or a production RAG engine.

## Engineering highlights

- Reusable `src/` package layout
- Lightweight document indexing with JSON persistence
- CLI and Gradio interfaces over shared application logic
- TXT and optional PDF document ingestion
- Resume ranking and reporting workflow examples
- Five Docker Compose services built from one image
- Synthetic sample data and deterministic local execution
- GitHub Actions, pytest, and Ruff checks
- No required API keys or outbound model calls

## Technology

`Python` · `Gradio` · `Docker Compose` · `pytest` · `Ruff` · `pypdf` · `CLI Applications` · `GitHub Actions`

## Included applications

| Application | Purpose | Default port |
| --- | --- | ---: |
| Retrieval demo | Query a small local corpus | 7860 |
| Document Q&A | Load TXT/PDF content and answer from retrieved passages | 7861 |
| Workflow chatbot | Demonstrate ticketing, scheduling, and retrieval fallback | 7862 |
| Resume shortlister | Rank synthetic resume records against a role | 7863 |
| Reporting demo | Generate Markdown, social copy, SVG, and JSON scheduling output | 7864 |

## Architecture

```text
CLI or Gradio application
          │
          ▼
Reusable pipeline modules
          │
          ├── document loading
          ├── tokenization and SimpleIndex
          ├── keyword/Jaccard retrieval
          └── application-specific formatting
          │
          ▼
Local result and generated artifacts
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest -q
```

Use the CLI:

```bash
llm-rag \
  --docs sample_data/capitals.txt \
  --query "What is the capital of Norway?" \
  -k 1
```

Persist and reload an index:

```bash
llm-rag --docs sample_data/capitals.txt --query "Capital of Japan" --save-index /tmp/index.json -k 2
llm-rag --load-index /tmp/index.json --query "Capital of Japan" -k 1
```

## Run the interfaces

```bash
PYTHONPATH=src python app/demo_gradio.py
PYTHONPATH=src python app/doc_qa.py
PYTHONPATH=src python app/chatbot.py
PYTHONPATH=src python app/resume_demo.py
PYTHONPATH=src python app/reporting_demo.py
```

The interfaces respect `GRADIO_SERVER_NAME` and `GRADIO_SERVER_PORT`.

## Docker Compose

```bash
docker compose up --build -d
```

Check the services:

```bash
for port in 7860 7861 7862 7863 7864; do
  curl -fsS "http://127.0.0.1:${port}" >/dev/null && echo "${port}: OK"
done
```

## Repository structure

```text
app/                 # Gradio entry points
src/llm_rag/         # Reusable retrieval and workflow modules
sample_data/         # Synthetic corpora and generated examples
scripts/             # Sample-data generators
tests/               # Unit and integration tests
docs/                # Architecture and demo notes
.github/workflows/   # Continuous integration
Dockerfile
docker-compose.yml
```

## Verification

```bash
pytest -q
python -m pip install ruff
ruff check --select=E9,F63,F7,F82 .
```

The CI workflow runs tests and critical Ruff rules on pushes and pull requests.

## Retrieval behavior

`SimpleIndex` tokenizes documents and ranks them using Jaccard-style token overlap. This makes the implementation:

- easy to inspect
- deterministic
- fast on small sample corpora
- suitable for learning, UI development, and pipeline testing

For semantic or production retrieval, replace it with an embedding model, chunking strategy, vector store, reranking, source citations, and evaluation dataset.

## Security and data

- sample inputs are synthetic or generated locally
- no secrets are required
- no external AI API is called
- generated indexes and reports may still contain source-document text and should be handled accordingly

## Project status

RAGworks is a compact application portfolio and offline integration test bed. It demonstrates packaging, retrieval interfaces, workflow automation, Gradio UX, containerization, tests, and CI while keeping the limitations of its retrieval method explicit.