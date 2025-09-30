import os

def test_sample_data_readme_exists():
    assert os.path.isfile(os.path.join("sample_data", "README.md"))


def test_readme_has_title():
    with open("README.md", "r", encoding="utf-8") as f:
        first = f.readline().strip()
    assert first.startswith("# AI & Automation Portfolio")


def test_requirements_mentions_pytest():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        text = f.read()
    assert "pytest" in text
