# src/main.py
from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

from agent.config import load_settings, project_root
from agent.planner.planner import run_planner
from agent.llm import make_client


def ask_user(prompt: str) -> str:
    return input(prompt).strip()

def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")

def main() -> None:
    settings = load_settings()

    user_prompt = ask_user("Describe the chip you want: ")
    
    client = make_client(settings)
    planner_response = run_planner(client, settings, user_prompt) # I put the option of client here in case we want to use different models/clients for each component
    planner_text_output = planner_response.choices[0].message.content or ""
    # print("\n" + "=" * 80)
    # print(planner_text_output)
    # print("=" * 80 + "\n")

    artifacts_dir = project_root() / "artifacts"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    write_json(
        artifacts_dir / f"planner_{ts}.json",
        {
            "timestamp": ts,
            "model": settings.model,
            "user_prompt": user_prompt,
            "planner_output": planner_text_output,
        },
    )

    print(f"Saved planner output to: {artifacts_dir}")

if __name__ == "__main__":
    main()