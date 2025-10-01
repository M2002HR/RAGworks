"""Gradio demo: Resume parsing & shortlisting (keyword-based, no external deps).

Run (src-layout friendly):
    PYTHONPATH=src python app/resume_demo.py
"""
from __future__ import annotations
import pathlib, sys
from typing import List, Optional

# src-layout safety
repo_root = pathlib.Path(__file__).resolve().parents[1]
src_path = repo_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import os
import gradio as gr  # noqa: E402
from llm_rag.resume import rank_resumes, load_resume_texts  # noqa: E402

# Fallback synthetic resumes for demo if no files uploaded
_SAMPLE_RESUMES = [
    "Jane Doe\nSkills: Python, SQL, Pandas, Docker\nBuilt ETL pipelines on AWS; dashboards in Power BI.",
    "John Roe\nSkills: Java, Kubernetes, Terraform\nImplemented microservices with gRPC; CI/CD with GitHub Actions.",
    "Alex Poe\nSkills: Python, FastAPI, React, PostgreSQL\nShipped internal tooling; data ingestion and REST APIs.",
]

def _run(job_desc: str, files: Optional[List[gr.File]], top_n: int):
    paths = [f.name for f in (files or []) if getattr(f, "name", None)]
    resumes = load_resume_texts(paths) or list(_SAMPLE_RESUMES)
    rows = rank_resumes(resumes, job_desc, top_n=top_n)
    # Convert to table-friendly rows
    headers = ["Candidate", "Score", "Matched Skills", "Preview"]
    table = [[f"Resume #{r['idx']}", r["score"], ", ".join(r["matched"]), r["preview"]] for r in rows]
    return headers, table


def create_resume_app() -> gr.Blocks:
    with gr.Blocks(title="RAGworks — Resume Shortlister (stub)") as demo:
        gr.Markdown("### Resume Shortlister (stub)\n_Keyword skills extraction; TXT/PDF supported (PDF optional)._")
        jd = gr.Textbox(label="Job Description", placeholder="e.g., Looking for Python + SQL + Docker")
        files = gr.Files(label="Upload resumes (TXT/PDF)", file_types=[".txt", ".pdf"])
        k = gr.Slider(1, 10, value=3, step=1, label="Top-N to show")
        default_headers = ["Candidate", "Score", "Matched Skills", "Preview"]
        out = gr.Dataframe(headers=default_headers, value=[], label="Ranked Candidates", interactive=False)

        def _update(job_desc, files, k):
            headers, table = _run(job_desc, files, k)
            out.headers = headers
            return table

        gr.Button("Rank").click(_update, inputs=[jd, files, k], outputs=[out], api_name=False)
    return demo


if __name__ == "__main__":
    app = create_resume_app()
    host = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    app.launch(server_name=host, server_port=port, show_api=False)
