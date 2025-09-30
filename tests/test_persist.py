import pathlib
import sys

# Ensure 'src' is on sys.path for the src/ layout
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from llm_rag.index_stub import SimpleIndex  # noqa: E402


def test_save_and_load_roundtrip(tmp_path):
    idx = SimpleIndex()
    idx.add_many(["Alpha Beta", "Paris France Eiffel", "Gamma"])
    save_path = tmp_path / "index.json"
    idx.save(save_path)

    reloaded = SimpleIndex.load(save_path)
    assert len(reloaded) == len(idx)
    q = "Eiffel Tower France"
    before = idx.search(q, k=1)[0]["text"]
    after = reloaded.search(q, k=1)[0]["text"]
    assert before == after


def test_from_dict_is_resilient_on_empty():
    reloaded = SimpleIndex.from_dict({"items": [], "next_id": 0, "format": 1})
    assert len(reloaded) == 0
