# src/agent/llm.py
from __future__ import annotations

from openai import OpenAI
from agent.config import Settings

def make_client(settings: Settings) -> OpenAI:
    return OpenAI(
        base_url=settings.base_url,
        api_key=settings.api_key,
    )
