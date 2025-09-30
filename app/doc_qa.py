"""Gradio demo: upload TXT/PDF files, ask a question, get a stub answer.

Run (src-layout friendly):
    PYTHONPATH=src python app/doc_qa.py
"""
from __future__ import annotations
import pathlib
import sys
from typing import List

# src-layout safety
repo_root = pathlib.Path(__file__).resolve().parents[1]
src_path = repo_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import gradio as gr  # noqa: E402
from llm_rag.docqa import qa_files  # noqa: E402


def _run(query: str, files: List[gr.File] | None, k: int) -> str:
    paths = [f.name for f in (files or []) if getattr(f, "name", None)]
    return qa_files(query, paths, k=k)


def create_docqa_app() -> gr.Blocks:
    with gr.Blocks(title="Document Q&A (stub)") as demo:
        gr.Markdown("### Document Q&A (keyword retrieval + stub answer)\n_TXT always; PDFs if PyPDF is present._")
        with gr.Row():
            q = gr.Textbox(label="Question", placeholder="e.g., What is the capital of Norway?")
            k = gr.Slider(1, 5, value=3, step=1, label="Top-K")
        files = gr.Files(label="Upload TXT/PDF files", file_types=[".txt", ".pdf"])
        out = gr.Textbox(label="Answer", lines=3)
        gr.Button("Ask").click(_run, inputs=[q, files, k], outputs=out)
    return demo


if __name__ == "__main__":
    app = create_docqa_app()
    app.launch()
