import pathlib
import sys

# Ensure 'src' is on sys.path for the src/ layout
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from llm_rag import SimpleIndex, answer  # noqa: E402


def test_index_retrieval_top_hit_and_pipeline():
    idx = SimpleIndex()
    docs = [
        "London is the capital of the United Kingdom.",
        "Paris is the capital of France and has the Eiffel Tower.",
        "Berlin has a vibrant technology scene.",
    ]
    idx.add_many(docs)
    q = "capital of France near the Eiffel Tower"
    hits = idx.search(q, k=2)
    assert len(hits) == 2
    assert any("Paris" in h["text"] for h in hits)
    out = answer(q, [h["text"] for h in hits])
    assert "Paris" in out


def test_index_accepts_mappings_and_is_stable_on_ties():
    idx = SimpleIndex()
    idx.add_many([{"text": "Alpha"}, {"text": "Beta"}, {"text": "Gamma"}])
    hits = idx.search("ZZZ", k=2)  # no overlaps => tie; should keep insertion order
    assert hits[0]["text"] == "Alpha"
    assert hits[1]["text"] == "Beta"
