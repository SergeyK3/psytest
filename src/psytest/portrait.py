from pathlib import Path
from typing import Iterable

def combine_blocks(blocks: Iterable[str]) -> str:
    header = "Психологический портрет сотрудника\n\n"
    return header + "\n\n".join(blocks)

def save_text(text: str, out_path: Path) -> Path:
    out_path.write_text(text, encoding="utf-8")
    return out_path
