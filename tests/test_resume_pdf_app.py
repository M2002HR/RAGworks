import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from llm_rag.pdfgen import make_pdf  # noqa: E402
from app.resume_demo import _run as resume_run  # noqa: E402


class DummyFile:
    def __init__(self, name):
        self.name = name


def test_resume_demo_can_rank_with_pdf_or_fallback(tmp_path):
    pdf_path = tmp_path / "resume.pdf"
    make_pdf(
        [
            "Jane Doe",
            "Skills: Python, SQL, Docker",
            "Experience: Built ETL pipelines on AWS.",
        ],
        pdf_path,
    )

    headers, table = resume_run(
        "Looking for Python and SQL with Docker",
        [DummyFile(str(pdf_path))],
        3,
    )

    assert isinstance(table, list) and table
    joined_rows = " ".join(", ".join(map(str, row)) for row in table)
    assert ("Python" in joined_rows) or ("python" in joined_rows)
