"""Lightweight keyword-matching RAG components, reusable across projects."""
from .rag_stub import answer
from .index_stub import SimpleIndex
from .pipeline import rag_pipeline, build_index
from .demo_app import create_demo
from .docqa import qa_files, load_texts_from_paths
from .chatbot import ChatOrchestrator, SimpleTicketStore, SimpleCalendar
from .resume import extract_skills, score_resume, rank_resumes, load_resume_texts

__all__ = [
    "answer","SimpleIndex","rag_pipeline","build_index","create_demo",
    "qa_files","load_texts_from_paths","ChatOrchestrator","SimpleTicketStore","SimpleCalendar",
    "extract_skills","score_resume","rank_resumes","load_resume_texts",
]
__version__ = "0.8.0"
