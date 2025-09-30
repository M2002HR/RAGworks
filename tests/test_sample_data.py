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


def test_cli_uses_repo_sample_data_capitals():
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    docs_path = repo_root / "sample_data" / "capitals.txt"
    assert docs_path.exists()
    rc, out = _run(["-q", "capital of Norway", "--docs", str(docs_path), "-k", "1"])
    assert rc == 0
    assert "Oslo" in out


def test_cli_finds_paris_from_eiffel_context():
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    docs_path = repo_root / "sample_data" / "capitals.txt"
    rc, out = _run(["-q", "Which city in France has the Eiffel Tower?", "--docs", str(docs_path), "-k", "1"])
    assert rc == 0
    assert "Paris" in out
