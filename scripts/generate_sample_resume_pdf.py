#!/usr/bin/env python3
"""Generate a synthetic resume PDF for demo/tests (no external deps).

Usage:
    python scripts/generate_sample_resume_pdf.py [OUTPUT_PATH]
Default OUTPUT_PATH: sample_data/resume_sample.pdf
"""
from __future__ import annotations
import sys
from pathlib import Path

from llm_rag.pdfgen import make_pdf

LINES = [
    "Jane Doe",
    "Skills: Python, SQL, Docker",
    "Projects: Internal tooling with FastAPI and PostgreSQL",
    "Experience: Data pipelines on AWS; dashboards in Power BI",
]


def main(argv=None):
    out = Path(argv[1]) if argv and len(argv) > 1 else Path("sample_data/resume_sample.pdf")
    path = make_pdf(LINES, out)
    print(f"wrote: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
