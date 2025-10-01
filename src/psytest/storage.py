from pathlib import Path
import json

def save_json(data, path: Path):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
