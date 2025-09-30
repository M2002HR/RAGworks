"""Standalone Gradio demo for the stub RAG answer().

- Loads sample_data/capitals.txt by default (one document per line).
- Uses llm_rag.rag_stub.answer(query, docs) with simple keyword match.
- No external APIs or secrets required.

Run:
    PYTHONPATH=src python app/demo_gradio.py
or (after editable install):
    python app/demo_gradio.py
"""
from __future__ import annotations

import pathlib
import sys
from typing import List

# Ensure src/ is on sys.path for 'src' layout when running directly
repo_root = pathlib.Path(__file__).resolve().parents[1]
src_path = repo_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import gradio as gr  # noqa: E402
from llm_rag.rag_stub import answer  # noqa: E402


SAMPLE_PATH = repo_root / "sample_data" / "capitals.txt"


def _load_docs(path: pathlib.Path = SAMPLE_PATH) -> List[str]:
    """Load documents (one per line) or return an empty list if missing."""
    if path.exists():
        lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines()]
        return [ln for ln in lines if ln]
    return []


def _run(query: str, docs_text: str, k: int) -> str:
    """Use provided docs_text (one per line) or fall back to sample_data."""
    docs = [ln.strip() for ln in docs_text.splitlines() if ln.strip()] or _load_docs()
    # Keep only top-k docs for the stub to mimic retrieval behaviour
    docs = docs[: max(1, int(k))]
    return answer(query, docs)


def create_app() -> gr.Blocks:
    with gr.Blocks(title="RAG Stub Demo") as demo:
        gr.Markdown("### RAG Stub Demo (keyword match)\n_No external APIs required._")
        with gr.Row():
            q = gr.Textbox(label="Query", placeholder="e.g., Which city in France has the Eiffel Tower?")
            k = gr.Slider(1, 5, value=2, step=1, label="Top-K docs")
        docs_tb = gr.Textbox(
            label="Docs (one per line; empty = use sample_data/capitals.txt)",
            value="",
            lines=6,
        )
        out = gr.Textbox(label="Answer", lines=3)
        gr.Button("Answer").click(_run, inputs=[q, docs_tb, k], outputs=out)
    return demo


if __name__ == "__main__":
    app = create_app()
    app.launch()
