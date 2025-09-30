import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import gradio as gr  # noqa: E402
from app.resume_demo import create_resume_app  # noqa: E402


def test_create_resume_app_returns_blocks():
    demo = create_resume_app()
    assert isinstance(demo, gr.Blocks)
