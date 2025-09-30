import pathlib
import sys

# Ensure 'src' is on sys.path for the src/ layout
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from llm_rag import answer  # noqa: E402


def test_selects_best_match():
    docs = [
        "London is the capital of the United Kingdom.",
        "Paris is the capital of France and is known for the Eiffel Tower.",
        "Berlin has a vibrant technology scene.",
    ]
    q = "What is the capital of France near the Eiffel Tower?"
    out = answer(q, docs)
    assert isinstance(out, str)
    assert "Paris" in out


def test_accepts_mapping_docs():
    docs = [{"text": "Rome is the capital of Italy."}, "Madrid is the capital of Spain."]
    out = answer("Which city is the capital of Italy?", docs)
    assert "Rome" in out


def test_handles_no_docs():
    out = answer("anything", [])
    assert "No documents provided" in out
