"""Document Q&A utilities (TXT always; PDF if optional backend available).

Zero external hard deps: PDF text extraction is attempted if `pypdf` is available;
otherwise PDFs are skipped with a note. This keeps the project minimal.

Public API:
- load_texts_from_paths(paths): list[str]  # TXT => one doc per line; PDF => small chunks
- qa_files(query, paths, k=3): str  -> runs retrieval + stub answer over file texts
"""
from __future__ import annotations
from typing import List, Sequence
from pathlib import Path
import re

from .pipeline import rag_pipeline, build_index


def _read_txt_lines(path: Path) -> List[str]:
    """Return non-empty lines; TXT is treated as one document per line."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return []
    lines = [ln.strip() for ln in text.splitlines()]
    return [ln for ln in lines if ln]


def _read_pdf_chunks(path: Path) -> List[str]:
    """Try to read PDF text with pypdf and split into small chunks; else return []."""
    try:
        import pypdf  # type: ignore
    except Exception:
        return []
    try:
        reader = pypdf.PdfReader(str(path))
        texts = []
        for page in getattr(reader, "pages", []):
            try:
                txt = page.extract_text() or ""
            except Exception:
                txt = ""
            if txt:
                texts.append(txt)
        text = "\n".join(texts).strip()
        if not text:
            return []
        # Naive chunking: split on blank lines, then on sentence-ish boundaries.
        rough_paras = re.split(r"\n{2,}", text)
        chunks: List[str] = []
        for para in rough_paras:
            for sent in re.split(r"(?<=[.!?])\s+", para.strip()):
                s = sent.strip()
                if s:
                    chunks.append(s)
        return chunks
    except Exception:
        return []


def load_texts_from_paths(paths: Sequence[str | Path]) -> List[str]:
    docs: List[str] = []
    for p in paths:
        path = Path(p)
        if not path.exists() or not path.is_file():
            continue
        ext = path.suffix.lower()
        if ext == ".txt":
            docs.extend(_read_txt_lines(path))
        elif ext == ".pdf":
            docs.extend(_read_pdf_chunks(path))
    # Fallback: if nothing loaded, try repo sample_data/capitals.txt (line-wise)
    if not docs:
        repo_root = Path(__file__).resolve().parents[2]
        sample = repo_root / "sample_data" / "capitals.txt"
        if sample.exists():
            docs.extend(_read_txt_lines(sample))
    return docs


def qa_files(query: str, paths: Sequence[str | Path], k: int = 3) -> str:
    """Build an index over file texts and return a stub answer via the existing pipeline."""
    docs_list = load_texts_from_paths(paths)
    if not docs_list:
        return "No readable documents found."
    idx = build_index(docs_list)
    return rag_pipeline(query, index=idx, k=max(1, int(k)))
