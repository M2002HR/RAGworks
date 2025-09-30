import pathlib


def test_docs_files_have_expected_sections():
    root = pathlib.Path(__file__).resolve().parents[1]
    readme = (root / "README.md").read_text(encoding="utf-8")
    architecture = (root / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8")
    demo = (root / "docs" / "DEMO.md").read_text(encoding="utf-8")

    assert "Quickstart" in readme
    assert "Architecture" in architecture.splitlines()[0]
    assert "Demo Guide" in demo.splitlines()[0]
    assert "docker compose up" in demo
