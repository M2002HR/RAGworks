"""Tiny pure-Python PDF generator (no deps).

Exports:
- make_pdf(lines: list[str], out_path: str) -> str  # writes a single-page PDF with each line as a text row.

Notes:
- This is not a full PDF library; it's a minimal writer sufficient for tests/demos.
"""
from __future__ import annotations
from pathlib import Path


def make_pdf(lines, out_path):
    out_path = Path(out_path)
    buf = bytearray()
    pos = 0
    offsets = {}

    def w(data):
        nonlocal pos
        if isinstance(data, str):
            data = data.encode("latin1")
        buf.extend(data)
        pos += len(data)

    def start_obj(num, body_bytes):
        offsets[num] = pos
        w(f"{num} 0 obj\n"); w(body_bytes); w("\nendobj\n")

    # Header
    w("%PDF-1.4\n%\xE2\xE3\xCF\xD3\n")

    # Font object
    start_obj(5, "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    # Contents stream
    y = 760
    contents = "BT\n/F1 12 Tf\n"
    first = True
    for line in lines:
        safe = line.replace("(", "\\(").replace(")", "\\)")
        if first:
            contents += f"50 {y} Td ({safe}) Tj\n"
            first = False
        else:
            contents += f"0 -18 Td ({safe}) Tj\n"
        y -= 18
    contents += "ET"
    contents_bytes = contents.encode("latin1")
    stream = f"<< /Length {len(contents_bytes)} >>\nstream\n".encode("latin1") + contents_bytes + b"\nendstream"
    offsets[4] = pos
    w("4 0 obj\n"); w(stream); w("\nendobj\n")

    # Page / Pages / Catalog
    start_obj(3, "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>")
    start_obj(2, "<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    start_obj(1, "<< /Type /Catalog /Pages 2 0 R >>")

    # xref table
    xref_pos = pos
    w("xref\n")
    size = 6  # 0..5 (we used 1..5)
    w(f"0 {size}\n")
    w("0000000000 65535 f \n")  # free obj 0
    for i in range(1, size):
        w(f"{offsets.get(i, 0):010} 00000 n \n")

    # trailer
    w("trailer\n"); w(f"<< /Size {size} /Root 1 0 R >>\n")
    w("startxref\n"); w(f"{xref_pos}\n"); w("%%EOF\n")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(buf)
    return str(out_path)
