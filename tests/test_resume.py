import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from llm_rag.resume import extract_skills, score_resume, rank_resumes, load_resume_texts  # noqa: E402


def test_extract_and_score_finds_overlap():
    resume = "Experienced engineer with Python, SQL, Docker; built ETL pipelines on AWS."
    jd = "We need a Python and SQL developer with Docker experience."
    s = score_resume(resume, jd)
    assert s["score"] >= 3
    assert set(["python","sql","docker"]).issubset(set(s["matched_skills"]))


def test_ranking_orders_best_first():
    resumes = [
        "Java developer with Kubernetes.",
        "Python developer with SQL and Docker.",
        "Beginner Python.",
    ]
    jd = "Looking for Python and SQL developer with Docker."
    rows = rank_resumes(resumes, jd, top_n=2)
    assert rows[0]["idx"] == 1  # the strongest match
    assert rows[0]["score"] >= rows[1]["score"]


def test_load_resume_texts_reads_txt(tmp_path):
    p1 = tmp_path / "a.txt"; p1.write_text("Python SQL", encoding="utf-8")
    p2 = tmp_path / "b.txt"; p2.write_text("Java", encoding="utf-8")
    out = load_resume_texts([str(p1), str(p2)])
    assert len(out) == 2 and "Python" in out[0]
