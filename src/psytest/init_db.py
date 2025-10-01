
from pathlib import Path
import sqlite3

def init_db(db_path: Path, schema_path: Path):
    con = sqlite3.connect(str(db_path))
    with open(schema_path, "r", encoding="utf-8") as f:
        con.executescript(f.read())
    con.commit()
    con.close()
    return db_path
