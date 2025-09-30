import pathlib
import sys

# Ensure 'src' is on sys.path for the src/ layout
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from llm_rag.docqa import qa_files, load_texts_from_paths  # noqa: E402
import gradio as gr  # noqa: F401  # ensure gradio importable for the demo


def test_qa_files_over_txt(tmp_path):
    p = tmp_path / "sample.txt"
    p.write_text("Oslo is the capital of Norway.\n", encoding="utf-8")
    out = qa_files("what is the capital of Norway?", [str(p)], k=1)
    assert "Oslo" in out


def test_loader_falls_back_to_sample_data_if_empty():
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    sample = repo_root / "sample_data" / "capitals.txt"
    assert sample.exists(), "sample_data/capitals.txt should exist for fallback"
    texts = load_texts_from_paths([])
    assert isinstance(texts, list) and len(texts) >= 1

def test_qa_files_over_multiline_txt_selects_correct_line(tmp_path):
    p = tmp_path / "multi.txt"
    p.write_text(
        "Paris is the capital of France and home to the Eiffel Tower.\n"
        "London is the capital of the United Kingdom.\n"
        "Oslo is the capital of Norway.\n",
        encoding="utf-8",
    )
    out = qa_files("what is the capital of Norway?", [str(p)], k=1)
    assert "Oslo" in out
