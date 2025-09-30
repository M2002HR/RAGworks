import pathlib


def test_ci_workflow_exists_and_is_reasonable():
    root = pathlib.Path(__file__).resolve().parents[1]
    wf = root / ".github" / "workflows" / "ci.yml"
    assert wf.exists(), "Expected .github/workflows/ci.yml to exist"
    text = wf.read_text(encoding="utf-8")
    # Basic sanity checks (no YAML parser required)
    assert "actions/checkout" in text
    assert "actions/setup-python" in text
    assert "pytest -q" in text
    assert "ruff check" in text
