import pathlib
import sys

repo_root = pathlib.Path(__file__).resolve().parents[1]
# Ensure repo root and 'src' are on sys.path
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(repo_root / "src"))

import gradio as gr  # noqa: E402
from app.demo_gradio import create_app, _load_docs  # noqa: E402


def test_create_app_returns_blocks():
    demo = create_app()
    assert isinstance(demo, gr.Blocks)


def test_load_docs_from_sample_data():
    sample = repo_root / "sample_data" / "capitals.txt"
    docs = _load_docs(sample)
    assert isinstance(docs, list)
    assert any("Oslo" in d or "Paris" in d for d in docs), "Expected sample capitals in docs"
