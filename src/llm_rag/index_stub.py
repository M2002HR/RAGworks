"""A minimal FAISS-like in-memory index (no external deps).

Provides `SimpleIndex` with add/add_many/search. Similarity is Jaccard overlap
over token sets; stable ordering on ties. Accepts strings or mappings with a
'text' key. Intended for demos and tests only.
"""
from __future__ import annotations
from typing import Sequence, Mapping, Union, List, Dict
import re

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
