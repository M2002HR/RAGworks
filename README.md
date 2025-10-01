# RAGworks

Minimal RAG + automation portfolio: CLI, Gradio demos, Docker, CI — no external APIs

[![CI](https://img.shields.io/github/actions/workflow/status/yourname/RAGworks/ci.yml?branch=main)](https://github.com/yourname/RAGworks/actions)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Licence](https://img.shields.io/badge/licence-MIT-green)

A compact, batteries-included AI & automation showcase. It bundles a reusable RAG stub, document Q&A, workflow chatbot, résumé shortlister, and reporting/content automation – each with Gradio demos, CLI entry points, Docker support, and continuous integration.

All examples use synthetic data only. Never commit secrets; use placeholders such as `OPENAI_API_KEY=PLACEHOLDER`.

---

## Contents
- [Features](#features)
- [Quickstart (local)](#quickstart-local)
- [CLI usage](#cli-usage)
- [Demos (Gradio)](#demos-gradio)
- [Docker (multi-service)](#docker-multi-service)
- [CI / lint / tests](#ci--lint--tests)
- [Project structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Security & data](#security--data)
- [Licence](#licence)

## Features
- **RAG core** – keyword-based `answer()` plus a light-weight `SimpleIndex` with JSON save/load helpers.
- **Demos and pipelines** – Gradio apps for RAG, document Q&A (TXT and optional PDF), chatbot (ticket/scheduling stubs), résumé ranking, and reporting (Markdown summary, short social post, SVG card, JSON scheduler).
- **Developer UX** – src-layout, editable install (`pip install -e .`), CLI (`llm-rag`), Docker Compose services, GitHub Actions.
- **Minimal dependencies** – Python stdlib and Gradio. PDF support is optional via `pypdf`.

## Quickstart (local)
```bash
pip install -r requirements.txt
pip install -e .
pytest -q
```

## CLI usage
```bash
# RAG answer using the sample corpus
llm-rag -q "What is the capital of Norway?" --docs sample_data/capitals.txt -k 1

# Persist and reload an index
llm-rag -q "Capital of Japan" --docs sample_data/capitals.txt --save-index /tmp/idx.json -k 2
llm-rag -q "Capital of Japan" --load-index /tmp/idx.json -k 1
```

Generate sample PDFs without extra dependencies:
```bash
python scripts/generate_sample_pdf.py sample_data/capitals.pdf
python scripts/generate_sample_resume_pdf.py sample_data/resume_sample.pdf
```

## Demos (Gradio)
```bash
# src-layout friendly launches
PYTHONPATH=src python app/demo_gradio.py       # RAG demo
PYTHONPATH=src python app/doc_qa.py            # Document Q&A (TXT/PDF)
PYTHONPATH=src python app/chatbot.py           # Chatbot (tickets, scheduling, RAG fallback)
PYTHONPATH=src python app/resume_demo.py       # Résumé shortlister
PYTHONPATH=src python app/reporting_demo.py    # Reporting & content automation
```
All demos respect `GRADIO_SERVER_NAME` and `GRADIO_SERVER_PORT`.

## Docker (multi-service)
A single image powers five services on distinct ports.
```bash
docker compose up --build -d
for p in 7860 7861 7862 7863 7864; do curl -sf http://localhost:$p >/dev/null && echo "port $p OK" || echo "port $p FAIL"; done
```
Ports: `7860` demo · `7861` document Q&A · `7862` chatbot · `7863` résumé · `7864` reporting.

If you prefer identical container ports, map host → container `7860` for each service in Compose and control the application via `GRADIO_SERVER_PORT`.

## CI / lint / tests
The workflow `.github/workflows/ci.yml` runs on every push, pull request, and manual dispatch. It caches pip, installs dependencies, runs `pytest -q`, then executes `ruff check --select=E9,F63,F7,F82 .`.

Locally:
```bash
pytest -q
python -m pip install ruff && ruff check --select=E9,F63,F7,F82 .
```

## Project structure
```text
app/                 Gradio demos (RAG, Doc Q&A, Chatbot, Résumé, Reporting)
src/llm_rag/         Reusable modules (rag_stub, index_stub, pipeline, docqa, chatbot, resume, reporting)
sample_data/         Synthetic corpora and generated artefacts (PDFs, SVG, JSON)
tests/               Smoke and integration tests (includes PDF generation)
Dockerfile, docker-compose.yml
.github/workflows/ci.yml
```

## Troubleshooting
- **Service unreachable on 7861/7863** – ensure `GRADIO_SERVER_PORT` is set per service; rebuild and run `docker compose up -d`.
- **Pip JSON decode errors during Docker build** – the Dockerfile forces the canonical PyPI index and retry logic. Behind a proxy, add trusted-host arguments.
- **PDF ingestion empty** – `pypdf` is optional; without it the loader falls back to `sample_data/capitals.txt`.

## FAQ
**Where does retrieval happen?** In `SimpleIndex.search()` (token-based Jaccard). `rag_pipeline()` wires the index into `rag_stub.answer()`.

**Can I persist the index?** Yes – `SimpleIndex.save()` and `SimpleIndex.load()`, or the CLI `--save-index/--load-index` flags.

**Are secrets required?** No. Use placeholders only; everything operates offline with synthetic content.

## Security & data
Use synthetic or auto-generated data located under `sample_data/` exclusively. The project makes no outbound API calls; optional PDF parsing remains local.

## Licence
MIT. Add a dedicated LICENCE file if required.

For deeper guidance, read `docs/ARCHITECTURE.md`, `docs/DEMO.md`, and `docs/index.md`.
