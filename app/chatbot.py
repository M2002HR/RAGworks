"""Gradio chat UI for the stub enterprise chatbot.

Run (src-layout friendly):
    PYTHONPATH=src python app/chatbot.py
"""
from __future__ import annotations
import pathlib
import sys

# src-layout safety
repo_root = pathlib.Path(__file__).resolve().parents[1]
src_path = repo_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import os
import gradio as gr  # noqa: E402
from llm_rag.chatbot import ChatOrchestrator  # noqa: E402

bot = ChatOrchestrator()


def _chat_fn(message: str, history):
    return bot.handle(message)


def create_chat_app() -> gr.Blocks:
    with gr.Blocks(title="RAGworks — Enterprise Chatbot (stub)") as demo:
        gr.Markdown("### Enterprise Chatbot (stub)\n_Tickets, scheduling, and RAG answers — no external APIs._")
        gr.ChatInterface(fn=_chat_fn, title="Chat")
    return demo


if __name__ == "__main__":
    app = create_chat_app()
    host = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    app.launch(server_name=host, server_port=port, show_api=False)
