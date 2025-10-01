import pathlib


def test_readme_has_sections_and_commands():
    root = pathlib.Path(__file__).resolve().parents[1]
    readme = (root / "README.md").read_text(encoding="utf-8")
    for key in [
        "# RAGworks",
        "Quickstart (local)",
        "CLI usage",
        "Docker (multi-service)",
        "CI / lint / tests",
        "Troubleshooting",
        "FAQ",
    ]:
        assert key in readme
    # Ensure multi-service ports are documented
    assert "7860" in readme and "7864" in readme


def test_docs_pages_link_and_contain_headers():
    root = pathlib.Path(__file__).resolve().parents[1]
    arch = (root / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8")
    demo = (root / "docs" / "DEMO.md").read_text(encoding="utf-8")
    index = (root / "docs" / "index.md").read_text(encoding="utf-8")
    assert "Architecture & Design" in arch
    assert "Demo Guide (precise)" in demo
    assert "Documentation Index" in index
    assert "doc_qa.py" in demo and "resume_demo.py" in demo
    sample = (root / "sample_data" / "README.md").read_text(encoding="utf-8")
    assert "synthetic" in sample.lower()
