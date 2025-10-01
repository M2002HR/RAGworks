import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from llm_rag.pdfgen import make_pdf  # noqa: E402
from llm_rag.docqa import load_texts_from_paths, qa_files  # noqa: E402


def test_make_pdf_and_load_with_or_without_pypdf(tmp_path):
    # 1) Create a PDF containing capitals lines
    pdf_path = tmp_path / "capitals.pdf"
    lines = [
        "Paris is the capital of France and home to the Eiffel Tower.",
        "Oslo is the capital of Norway.",
    ]
    make_pdf(lines, pdf_path)

    # 2) Try to load texts from the PDF
    texts = load_texts_from_paths([str(pdf_path)])
    # If pypdf is installed, PDF text should be non-empty; else loader returns []
    if texts:
        joined = " ".join(texts)
        assert "Oslo" in joined or "Norway" in joined
    else:
        # Fallback path: qa_files should still answer via sample_data fallback
        out = qa_files("what is the capital of Norway?", [str(pdf_path)], k=1)
        assert "Oslo" in out
