"""Resume parsing & ranking (minimal, no external deps).

Features:
- `extract_skills(text, skill_lexicon=None)` -> set[str]
- `score_resume(text, job_desc, skill_lexicon=None)` -> dict(score, matched_skills)
- `rank_resumes(resume_texts, job_desc, top_n=5, skill_lexicon=None)` -> list[dict]
- `load_resume_texts(paths)` -> list[str] (TXT only by default; PDF via pypdf if available)

Notes:
- This is a simple keyword-based matcher; no PII processing; use only synthetic data in tests/demos.
"""
from __future__ import annotations
from typing import Iterable, List, Sequence, Set, Dict, Optional
from pathlib import Path
import re

# Default lexicon (extend as needed)
DEFAULT_SKILLS: Set[str] = {
    "python","java","javascript","typescript","sql","postgres","mysql","sqlite",
    "aws","gcp","azure","docker","kubernetes","terraform",
    "linux","bash","git",
    "pandas","numpy","scikit-learn","sklearn","ml","machine learning","data engineering",
    "fastapi","flask","django","react","node","grpc","rest","api","airflow","spark","hadoop",
    "excel","power bi","tableau"
}

_WORD_RE = re.compile(r"[a-z0-9]+")

def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()

def _token_set(text: str) -> Set[str]:
    return set(_WORD_RE.findall(text.lower()))

def extract_skills(text: str, skill_lexicon: Optional[Iterable[str]] = None) -> Set[str]:
    """Extract skills by keyword match (single- and multi-word)."""
    skills = set(s.strip().lower() for s in (skill_lexicon or DEFAULT_SKILLS))
    tokens = _token_set(text)
    norm = _normalise(text)
    matched: Set[str] = set()
    for s in skills:
        if " " in s:  # multi-word phrase
            if s in norm:
                matched.add(s)
        else:
            if s in tokens:
                matched.add(s)
    return matched

def score_resume(text: str, job_desc: str, skill_lexicon: Optional[Iterable[str]] = None) -> Dict:
    """Score by overlap between resume skills and job description skills."""
    job_skills = extract_skills(job_desc, skill_lexicon)
    res_skills = extract_skills(text, skill_lexicon)
    matched = sorted(res_skills & job_skills)
    score = len(matched)
    return {"score": score, "matched_skills": matched, "job_skills": sorted(job_skills)}

def rank_resumes(resume_texts: Sequence[str], job_desc: str, top_n: int = 5, skill_lexicon: Optional[Iterable[str]] = None) -> List[Dict]:
    rows: List[Dict] = []
    for i, txt in enumerate(resume_texts):
        s = score_resume(txt, job_desc, skill_lexicon)
        rows.append({
            "idx": i,
            "score": s["score"],
            "matched": s["matched_skills"],
            "preview": (txt.strip().replace("\n", " ")[:120] + ("..." if len(txt) > 120 else "")),
        })
    rows.sort(key=lambda r: (-r["score"], r["idx"]))
    return rows[: max(1, int(top_n))]

def _read_txt(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""

def _read_pdf(path: Path) -> str:
    try:
        import pypdf  # optional
    except Exception:
        return ""
    try:
        reader = pypdf.PdfReader(str(path))
        pages = []
        for p in getattr(reader, "pages", []):
            try:
                pages.append(p.extract_text() or "")
            except Exception:
                pages.append("")
        return "\n".join(pages).strip()
    except Exception:
        return ""

def load_resume_texts(paths: Sequence[str | Path]) -> List[str]:
    out: List[str] = []
    for p in paths:
        path = Path(p)
        if not path.exists() or not path.is_file():
            continue
        ext = path.suffix.lower()
        if ext == ".txt":
            t = _read_txt(path)
        elif ext == ".pdf":
            t = _read_pdf(path)
        else:
            t = ""
        t = (t or "").strip()
        if t:
            out.append(t)
    return out
