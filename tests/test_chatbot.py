import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from llm_rag.chatbot import ChatOrchestrator  # noqa: E402


def test_ticket_intent_creates_id():
    bot = ChatOrchestrator(docs=["Alpha", "Beta"])
    out = bot.handle("please create a ticket for a login bug")
    assert "TICKET-" in out and "Created" in out


def test_schedule_intent_returns_stub_confirmation():
    bot = ChatOrchestrator(docs=["Alpha", "Beta"])
    out = bot.handle("can you schedule a meeting for product review?")
    assert "Scheduled" in out and "(stub)" in out


def test_qa_intent_uses_rag_fallback_with_sample_data():
    # With default sample_data, this should surface Oslo for the query.
    bot = ChatOrchestrator()
    out = bot.handle("what is the capital of Norway?")
    assert "Oslo" in out
