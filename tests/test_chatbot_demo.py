import pathlib
import sys

repo_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(repo_root / "src"))

import gradio as gr  # noqa: E402
from app.chatbot import create_chat_app  # noqa: E402


def test_create_chat_app_returns_blocks():
    demo = create_chat_app()
    assert isinstance(demo, gr.Blocks)
