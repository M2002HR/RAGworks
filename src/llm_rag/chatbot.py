"""Stub enterprise chatbot: intent routing + simple actions + RAG fallback.

- Ticket stub: creates synthetic IDs like TICKET-1, TICKET-2, ...
- Calendar stub: returns a deterministic scheduled string (no real time parsing).
- QA fallback: uses existing retrieval pipeline over sample_data (one line = one doc).

No external APIs, no secrets. Reusable across projects.
"""
from __future__ import annotations
from typing import List, Optional, Sequence
from pathlib import Path

from .pipeline import build_index, rag_pipeline

SAMPLE_FILE = Path(__file__).resolve().parents[2] / "sample_data" / "capitals.txt"


def _load_line_docs(path: Path) -> List[str]:
    if path.exists():
        lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines()]
        return [ln for ln in lines if ln]
    return []


class SimpleTicketStore:
    _counter = 0

    @classmethod
    def create_ticket(cls, summary: str) -> str:
        cls._counter += 1
        return f"TICKET-{cls._counter}: {summary.strip()[:60]}"


class SimpleCalendar:
    @staticmethod
    def schedule(title: str, when_text: Optional[str] = None) -> str:
        # Deterministic placeholder to keep tests stable.
        suffix = f" at 09:00" if when_text else " at 10:00"
        return f"Scheduled '{title.strip() or 'Meeting'}'{suffix} (stub)"


class ChatOrchestrator:
    def __init__(self, docs: Optional[Sequence[str]] = None) -> None:
        self.docs = list(docs) if docs is not None else _load_line_docs(SAMPLE_FILE)
        self.index = build_index(self.docs or ["Paris is the capital of France."])

    @staticmethod
    def _intent(text: str) -> str:
        t = text.lower()
        if any(k in t for k in ("ticket", "bug", "issue", "incident")):
            return "ticket"
        if any(k in t for k in ("schedule", "meeting", "calendar", "book a meeting")):
            return "schedule"
        return "qa"

    def handle(self, message: str) -> str:
        it = self._intent(message)
        if it == "ticket":
            tid = SimpleTicketStore.create_ticket(message)
            return f"Created {tid} (stub)."
        if it == "schedule":
            return SimpleCalendar.schedule(message, when_text=None)
        # QA fallback via retrieval + stub answer
        return rag_pipeline(message, index=self.index, k=3)


__all__ = ["ChatOrchestrator", "SimpleTicketStore", "SimpleCalendar"]
