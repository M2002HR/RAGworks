import pathlib
import sys

# Ensure 'src' is on sys.path for the src/ layout
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from llm_rag.pipeline import rag_pipeline, build_index  # noqa: E402
from llm_rag.demo_app import create_demo  # noqa: E402
import gradio as gr  # noqa: E402


def test_rag_pipeline_returns_expected_snippet():
    docs = [
        "Paris is the capital of France and home to the Eiffel Tower.",
        "Rome is the capital of Italy.",
    ]
    idx = build_index(docs)
    out = rag_pipeline("Which city in France has the Eiffel Tower?", index=idx, k=1)
    assert isinstance(out, str)
    assert "Paris" in out


def test_create_demo_returns_blocks():
    demo = create_demo()
    assert isinstance(demo, gr.Blocks)
