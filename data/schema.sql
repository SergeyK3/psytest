
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    tests TEXT NOT NULL,     -- JSON list of test_ids
    user_hash TEXT           -- optional anonymized user id
);

CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    test_id TEXT NOT NULL,
    item_id INTEGER NOT NULL,
    answer INTEGER NOT NULL,
    ts TEXT NOT NULL,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    test_id TEXT NOT NULL,
    scale TEXT NOT NULL,
    raw REAL NOT NULL,
    norm REAL,
    ts TEXT NOT NULL,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);
