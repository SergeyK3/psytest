from pathlib import Path

BASE = Path(__file__).resolve().parents[2] / "data" / "prompts"

def load_prompt(name: str) -> str:
    path = BASE / name
    return path.read_text(encoding="utf-8")
