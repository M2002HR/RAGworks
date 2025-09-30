"""A minimal FAISS-like in-memory index (no external deps).

Provides `SimpleIndex` with add/add_many/search and JSON save/load.
Similarity is Jaccard overlap over token sets; stable ordering on ties.
Accepts strings or mappings with a 'text' key. Intended for demos and tests only.
"""
from __future__ import annotations
from typing import Sequence, Mapping, Union, List, Dict, Any
import re
import json
from pathlib import Path

Doc = Union[str, Mapping]
_WORD_RE = re.compile(r"[A-Za-z0-9]+")

def _tokenise(text: str) -> set[str]:
    return set(_WORD_RE.findall(text.lower()))

def _to_text(doc: Doc) -> str:
    if isinstance(doc, str):
        return doc
    if isinstance(doc, Mapping):
        return str(doc.get("text", ""))
    return str(doc)

class SimpleIndex:
    def __init__(self) -> None:
        self._items: List[tuple[int, str, set[str]]] = []
        self._next_id: int = 0

    def __len__(self) -> int:
        return len(self._items)

    def add(self, doc: Doc) -> int:
        text = _to_text(doc)
        tokens = _tokenise(text)
        doc_id = self._next_id
        self._next_id += 1
        self._items.append((doc_id, text, tokens))
        return doc_id

    def add_many(self, docs: Sequence[Doc]) -> List[int]:
        return [self.add(d) for d in docs]

    def search(self, query: str, k: int = 3) -> List[Dict]:
        q = _tokenise(query)
        scored = []
        for doc_id, text, tokens in self._items:
            if not q and not tokens:
                sim = 1.0
            elif not q or not tokens:
                sim = 0.0
            else:
                sim = len(q & tokens) / float(len(q | tokens))
            scored.append((sim, doc_id, text))
        scored.sort(key=lambda t: (-t[0], t[1]))  # high similarity first; stable by id on ties
        out = [{"id": did, "text": txt, "score": float(round(sim, 6))} for sim, did, txt in scored[:k]]
        return out

    # ---- Persistence (JSON) ----
    def to_dict(self) -> Dict[str, Any]:
        return {
            "next_id": self._next_id,
            "items": [{"id": doc_id, "text": text} for (doc_id, text, _tokens) in self._items],
            "format": 1,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SimpleIndex":
        obj = cls()
        items = data.get("items", []) or []
        for item in items:
            doc_id = int(item["id"])
            text = str(item["text"])
            tokens = _tokenise(text)
            obj._items.append((doc_id, text, tokens))
        if items:
            max_id = max(int(item["id"]) for item in items)
            obj._next_id = max(max_id + 1, int(data.get("next_id", max_id + 1)))
        else:
            obj._next_id = int(data.get("next_id", 0))
        return obj

    def save(self, path: Union[str, Path]) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: Union[str, Path]) -> "SimpleIndex":
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)
