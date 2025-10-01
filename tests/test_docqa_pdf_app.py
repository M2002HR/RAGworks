import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from llm_rag.pdfgen import make_pdf  # noqa: E402
from app.doc_qa import _run as docqa_run  # noqa: E402


class DummyFile:
    def __init__(self, name):
        self.name = name


def test_docqa_handles_pdf_or_fallback(tmp_path):
    pdf_path = tmp_path / "capitals.pdf"
    make_pdf(
        [
            "Paris is the capital of France and home to the Eiffel Tower.",
            "Oslo is the capital of Norway.",
        ],
        pdf_path,
    )

    out = docqa_run("what is the capital of Norway?", [DummyFile(str(pdf_path))], 3)
    assert "Oslo" in out
