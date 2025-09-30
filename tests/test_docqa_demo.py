import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import gradio as gr  # noqa: E402
from app.doc_qa import create_docqa_app  # noqa: E402


def test_create_docqa_app_returns_blocks():
    demo = create_docqa_app()
    assert isinstance(demo, gr.Blocks)
