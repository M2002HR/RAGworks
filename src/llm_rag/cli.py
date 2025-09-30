"""Minimal CLI for the stub RAG pipeline (no external APIs)."""

from __future__ import annotations
from typing import List, Optional
import argparse
from pathlib import Path

from .pipeline import rag_pipeline, build_index
from .index_stub import SimpleIndex

_SAMPLE_DOCS = [
    "Paris is the capital of France and home to the Eiffel Tower.",
    "London is the capital of the United Kingdom.",
    "Berlin has a vibrant technology scene and historic landmarks.",
]

def _load_docs(path: Optional[str]) -> List[str]:
    if not path:
        return list(_SAMPLE_DOCS)
    p = Path(path)
    if not p.exists():
        return list(_SAMPLE_DOCS)
    lines = [ln.strip() for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return lines or list(_SAMPLE_DOCS)

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Query a tiny keyword-based RAG stub.")
    parser.add_argument("-q", "--query", required=True, help="Your question.")
    parser.add_argument("--docs", type=str, default=None, help="Path to a UTF-8 text file, one document per line.")
    parser.add_argument("-k", type=int, default=2, help="Top-K documents to use (default: 2).")
    parser.add_argument("--save-index", type=str, default=None, help="Path to save JSON index after building.")
    parser.add_argument("--load-index", type=str, default=None, help="Path to load JSON index instead of building.")
    args = parser.parse_args(argv)

    idx: SimpleIndex
    if args.load_index and Path(args.load_index).exists():
        idx = SimpleIndex.load(args.load_index)
    else:
        docs = _load_docs(args.docs)
        idx = build_index(docs)
        if args.save_index:
            idx.save(args.save_index)

    out = rag_pipeline(args.query, index=idx, k=max(1, int(args.k)))
    print(out)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
