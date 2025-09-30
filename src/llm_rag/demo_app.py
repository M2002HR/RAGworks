"""Minimal Gradio demo for the stub RAG pipeline."""
from __future__ import annotations
import gradio as gr
from .pipeline import rag_pipeline, build_index

_SAMPLE_DOCS = [
    "Paris is the capital of France and home to the Eiffel Tower.",
    "London is the capital of the United Kingdom.",
    "Berlin has a vibrant technology scene and historic landmarks.",
]

def _run(query: str, docs_text: str, k: int) -> str:
    docs = [line.strip() for line in docs_text.splitlines() if line.strip()]
    idx = build_index(docs or _SAMPLE_DOCS)
    return rag_pipeline(query, index=idx, k=int(k))

def create_demo() -> gr.Blocks:
    with gr.Blocks(title="RAG Stub Demo") as demo:
        gr.Markdown("### RAG Stub Demo (no external APIs)")
        with gr.Row():
            query = gr.Textbox(label="Query", placeholder="e.g., What is the capital of France?")
        docs_text = gr.Textbox(
            label="Docs (one per line)",
            value="\n".join(_SAMPLE_DOCS),
            lines=6,
        )
        k = gr.Slider(1, 5, value=2, step=1, label="Top-K")
        out = gr.Textbox(label="Answer", lines=3)
        btn = gr.Button("Search")
        btn.click(_run, inputs=[query, docs_text, k], outputs=[out])
    return demo

if __name__ == "__main__":
    app = create_demo()
    app.launch()
