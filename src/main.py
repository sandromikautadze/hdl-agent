# src/main.py
from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime
from openai import OpenAI
from agent.config import load_settings, project_root
from agent.llm import make_client
from agent.prompts import BASE_SYSTEM_PROMPT


# HELPERS
def ask_user(prompt: str) -> str:
    return input(prompt).strip()

def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
    
def split_response(text: str) -> tuple[str, str, str]:
    reasoning_tag = "===REASONING_NOTES==="
    spec_tag = "===INTERNAL_SPEC_JSON==="
    user_tag = "===USER_SUMMARY==="

    if reasoning_tag not in text or spec_tag not in text or user_tag not in text:
        raise RuntimeError("Model response missing required delimiters.")

    reasoning = text.split(reasoning_tag, 1)[1].split(spec_tag, 1)[0].strip()
    json_part = text.split(spec_tag, 1)[1].split(user_tag, 1)[0].strip()
    user_part = text.split(user_tag, 1)[1].strip()
    return reasoning, user_part, json_part



def main() -> None:
    settings = load_settings()

    user_prompt = ask_user("Describe the chip you want: ")
    print("\nThinking...\n", flush=True)
    
    client = make_client(settings)
    if isinstance(client, OpenAI):
        response = client.chat.completions.create(
            model=settings.model, 
            messages=[
                {
                    "role": "system", 
                    "content": BASE_SYSTEM_PROMPT                    
                },
                {
                    "role": "user", 
                    "content": user_prompt
                }
            ]
        ) 
        
        text_response = response.choices[0].message.content
        
    else:
        raise NotImplementedError("Only valid client is OpenAI.")    

    reasoning, user_summary, internal_json_str = split_response(text_response)
    print(user_summary, flush=True)

    internal_spec = json.loads(internal_json_str)
    artifacts_dir = project_root() / "artifacts"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    write_json(
    artifacts_dir / f"spec_{ts}.json",
    {
        "timestamp": ts,
        "model": settings.model,
        "user_prompt": user_prompt,
        "reasoning_notes": reasoning,
        "user_summary": user_summary,
        "internal_spec": internal_spec,
    },
)


if __name__ == "__main__":
    main()