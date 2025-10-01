"""Gradio demo: reporting & content automation (stub).

Run (src-layout friendly):
    PYTHONPATH=src python app/reporting_demo.py
"""
from __future__ import annotations
import pathlib, sys, json as _json

# src-layout safety
repo_root = pathlib.Path(__file__).resolve().parents[1]
src_path = repo_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import os
import gradio as gr  # noqa: E402
from llm_rag.reporting import (  # noqa: E402
    generate_daily_report, generate_social_post,
    render_social_card_svg, schedule_post, load_queue
)

_SAMPLE_METRICS = {"visitors": 120, "signups": 7, "errors": 0}
_SAMPLE_HIGHLIGHTS = ["Launched the demo", "Added Document Q&A", "Zero prod errors"]


def _generate(metrics_json: str, highlights_text: str, date_str: str):
    try:
        metrics = _json.loads(metrics_json) if metrics_json.strip() else dict(_SAMPLE_METRICS)
        if not isinstance(metrics, dict):
            metrics = dict(_SAMPLE_METRICS)
    except Exception:
        metrics = dict(_SAMPLE_METRICS)
    highlights = [ln.strip() for ln in highlights_text.splitlines() if ln.strip()] or list(_SAMPLE_HIGHLIGHTS)
    md = generate_daily_report(metrics, highlights, date_str=date_str or None)
    post = generate_social_post(md)
    return md, post


def _make_card(title: str, subtitle: str):
    out_path = str(repo_root / "sample_data" / "social_card.svg")
    p = render_social_card_svg(title or "Daily Report", subtitle or "automation & ai", out_path)
    return p


def _schedule(post_text: str, when_iso: str, assets_path: str, queue_path: str):
    assets = [assets_path] if assets_path.strip() else []
    entry = schedule_post(post_text, when_iso=when_iso or "2025-01-01T09:00:00Z", assets=assets, queue_path=queue_path or "schedule.json")
    return _json.dumps(entry, ensure_ascii=False, indent=2)


def create_reporting_app() -> gr.Blocks:
    with gr.Blocks(title="Reporting & Content Automation (stub)") as demo:
        gr.Markdown("### Reporting & Content Automation (stub)\n_Generate a daily Markdown report, a social post, an SVG card, and queue a scheduled post (JSON)._"
        )

        with gr.Tab("Report + Post"):
            metrics = gr.Textbox(label="Metrics as JSON", value=_json.dumps(_SAMPLE_METRICS), lines=5)
            highlights = gr.Textbox(label="Highlights (one per line)", value="\n".join(_SAMPLE_HIGHLIGHTS), lines=5)
            date_str = gr.Textbox(label="Date (YYYY-MM-DD, optional)", value="")
            md = gr.Markdown(label="Report (Markdown)")
            post = gr.Textbox(label="Social Post", lines=3)
            gr.Button("Generate").click(_generate, inputs=[metrics, highlights, date_str], outputs=[md, post], api_name=False)

        with gr.Tab("Social Card"):
            title = gr.Textbox(label="Title", value="Daily Report")
            subtitle = gr.Textbox(label="Subtitle", value="automation & ai")
            svg_path = gr.Textbox(label="Saved SVG Path", interactive=False)
            gr.Button("Render Card").click(_make_card, inputs=[title, subtitle], outputs=[svg_path], api_name=False)

        with gr.Tab("Schedule"):
            post_text = gr.Textbox(label="Post text", value="Daily update: Launched the demo. #automation #ai", lines=3)
            when_iso = gr.Textbox(label="When (ISO 8601)", value="2025-01-01T09:00:00Z")
            assets_path = gr.Textbox(label="Asset path (optional)", value=str(repo_root / "sample_data" / "social_card.svg"))
            queue_path = gr.Textbox(label="Queue file path", value=str(repo_root / "sample_data" / "schedule.json"))
            scheduled = gr.Code(label="Scheduled Entry (JSON)", language="json")
            gr.Button("Schedule Post").click(_schedule, inputs=[post_text, when_iso, assets_path, queue_path], outputs=[scheduled], api_name=False)
    return demo


if __name__ == "__main__":
    app = create_reporting_app()
    host = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    app.launch(server_name=host, server_port=port, show_api=False)
