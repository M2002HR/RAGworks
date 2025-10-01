#!/usr/bin/env python3
"""Generate a sample PDF with world-capitals lines for Doc Q&A tests.

Usage:
    python scripts/generate_sample_pdf.py [OUTPUT_PATH]

Default OUTPUT_PATH: sample_data/capitals.pdf
"""
from __future__ import annotations
import sys
from pathlib import Path

from llm_rag.pdfgen import make_pdf

LINES = [
    "Paris is the capital of France and home to the Eiffel Tower.",
    "London is the capital of the United Kingdom.",
    "Berlin has a vibrant technology scene and historic landmarks.",
    "Oslo is the capital of Norway.",
    "Stockholm is the capital of Sweden.",
    "Rome is the capital of Italy.",
    "Madrid is the capital of Spain.",
    "Tokyo is the capital of Japan.",
    "Canberra is the capital of Australia.",
    "Ottawa is the capital of Canada.",
]


def main(argv=None):
    out = Path(argv[1]) if argv and len(argv) > 1 else Path("sample_data/capitals.pdf")
    path = make_pdf(LINES, out)
    print(f"wrote: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
