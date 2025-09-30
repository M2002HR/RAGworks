# portfolio-foundation

[![CI](https://img.shields.io/github/actions/workflow/status/yourname/portfolio-foundation/ci.yml?branch=main)](https://github.com/yourname/portfolio-foundation/actions)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A compact AI & Automation portfolio repo that ships a reusable RAG stub, CLI, Gradio demo, Docker setup, and CI pipeline.
**No external APIs are required**; keep secrets as placeholders like `OPENAI_API_KEY=PLACEHOLDER` for demos.

## Quickstart
```bash
# 1) Install
pip install -r requirements.txt
pip install -e .

# 2) Run tests
pytest -q
```

## Run the CLI
```bash
python -m llm_rag.cli -q "Which city in France has the Eiffel Tower?"
```
Use `--docs sample_data/capitals.txt` to point at the bundled corpus or `--save-index/--load-index` for caching.

## Launch the Gradio demo
```bash
PYTHONPATH=src python app/demo_gradio.py
```
Then open http://localhost:7860/. The demo falls back to `sample_data/capitals.txt` if the textarea is empty.

## Docker
```bash
docker compose up --build
```
This serves the Gradio demo on port 7860 using the bundled requirements.

## Documentation
- [Architecture](docs/ARCHITECTURE.md) — explains the modules, pipelines, and data flow.
- [Demo](docs/DEMO.md) — lists CLI, Gradio, and Docker usage tips.

## Project structure
- `src/llm_rag/` — Keyword-based RAG stub, SimpleIndex, pipeline utilities, CLI, and demo helpers.
- `app/demo_gradio.py` — Standalone Blocks app wired into the pipeline.
- `sample_data/` — Synthetic corpora (capitals) for demos/tests.
- `tests/` — Pytest smoke tests covering pipeline, CLI, demo, Docker, and docs.
- `docs/` — Expanded documentation referenced above.

> Prefer British English spelling when practical.
