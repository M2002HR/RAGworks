# Demo Guide

This guide explains how to interact with the RAG stub via CLI, Gradio, and Docker.

## Prerequisites
- Python 3.10+
- `pip install -r requirements.txt`
- `pip install -e .`

## CLI usage
```bash
python -m llm_rag.cli -q "capital of France" --docs sample_data/capitals.txt -k 2
```
Flags:
- `--docs PATH` — load documents from a UTF-8 file (one per line).
- `--save-index PATH` — serialise the index to JSON after building.
- `--load-index PATH` — skip building by loading a previous JSON index.

## Gradio web demo
```bash
PYTHONPATH=src python app/demo_gradio.py
```
Open http://localhost:7860/ and submit a query. Leaving the docs box empty uses the bundled capitals corpus. Adjust `Top-K docs` slider to change retrieval depth.

## Docker
```bash
docker compose up --build
```
This builds the slim Python image, installs dependencies, and exposes the demo on port 7860. The container relies on the same placeholders (`OPENAI_API_KEY=PLACEHOLDER`).

## Sample data
`sample_data/capitals.txt` contains synthetic sentences about world capitals for reproducible demos/tests. Replace or extend it with your own corpus as needed.
