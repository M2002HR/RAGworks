import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import gradio as gr  # noqa: E402
from app.reporting_demo import create_reporting_app  # noqa: E402


def test_create_reporting_app_returns_blocks():
    demo = create_reporting_app()
    assert isinstance(demo, gr.Blocks)
