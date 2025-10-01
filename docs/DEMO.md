# Demo Guide (precise)

## Local runs
```bash
PYTHONPATH=src python app/demo_gradio.py
PYTHONPATH=src python app/doc_qa.py
PYTHONPATH=src python app/chatbot.py
PYTHONPATH=src python app/resume_demo.py
PYTHONPATH=src python app/reporting_demo.py
```
Every demo respects `GRADIO_SERVER_NAME` and `GRADIO_SERVER_PORT` when provided.

## Docker (multi-service)
```bash
docker compose up --build -d
for p in 7860 7861 7862 7863 7864; do curl -sf http://localhost:$p >/dev/null && echo "port $p OK" || echo "port $p FAIL"; done
```
Services: 7860 demo · 7861 document Q&A · 7862 chatbot · 7863 résumé · 7864 reporting.

## CLI examples
```bash
llm-rag -q "What is the capital of Norway?" --docs sample_data/capitals.txt -k 1
llm-rag -q "Capital of Japan" --docs sample_data/capitals.txt --save-index /tmp/idx.json -k 2
llm-rag -q "Capital of Japan" --load-index /tmp/idx.json -k 1
```

## Document Q&A
Upload TXT (one document per line) or PDF (parsed when `pypdf` is installed). If nothing is readable, the loader falls back to `sample_data/capitals.txt`.

## Chatbot
Sample prompts:
- “Create a ticket for login bug” → ticket reference.
- “Schedule a meeting tomorrow at 10” → scheduled stub entry.
Other prompts flow to the RAG fallback.

## Résumé shortlister
Upload TXT/PDF résumés, provide a job description, and view ranked candidates by skill overlap.

## Reporting & content
Produce a Markdown daily report, generate a short social post, render an SVG social card, and append a JSON scheduling entry.
