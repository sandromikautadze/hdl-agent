from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

def project_root() -> Path:
    return Path(__file__).resolve().parents[2]

@dataclass(frozen=True)
class Settings:
    base_url: str
    api_key: str
    model: str

def load_settings(env_file: Path | None = None) -> Settings:
    root = project_root()
    env_path = env_file or (root / ".env")
    load_dotenv(env_path)

    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3-nano-30b-a3b:free")

    if not api_key or not base_url or not model:
        raise RuntimeError("Missing environment variable (set it in .env).")

    return Settings(base_url=base_url, api_key=api_key, model=model)