# src/agent/planner/planner.py
from __future__ import annotations

from agent.config import Settings
from agent.planner.prompts import PLANNER_SYSTEM


def run_planner(client, settings: Settings, user_prompt: str) -> str:
    messages = [
        {"role": "system", "content": PLANNER_SYSTEM},
        {"role": "user", "content": user_prompt},
    ]

    resp = client.chat.completions.create(
        model=settings.model,
        messages=messages,
    )

    return resp 