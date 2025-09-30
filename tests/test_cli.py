import pathlib
import sys
import contextlib
import io

# Ensure 'src' is on sys.path for the src/ layout
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from llm_rag.cli import main as cli_main  # noqa: E402


def _run(args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = cli_main(args)
    return rc, buf.getvalue()


def test_cli_basic_uses_sample_docs_and_finds_paris():
    rc, out = _run(["-q", "Which city in France has the Eiffel Tower?"])
    assert rc == 0
    assert "Paris" in out


def test_cli_reads_docs_file(tmp_path):
    docs_path = tmp_path / "docs.txt"
    docs_path.write_text("Rome is the capital of Italy.\nMadrid is the capital of Spain.\n", encoding="utf-8")
    rc, out = _run(["-q", "capital of Italy", "--docs", str(docs_path), "-k", "1"])
    assert rc == 0
    assert "Rome" in out
