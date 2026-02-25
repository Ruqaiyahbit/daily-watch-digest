import sqlite3

def get_conn(db_path: str):
    return sqlite3.connect(db_path)

def init_db(db_path: str):
    conn = get_conn(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider TEXT NOT NULL,
            external_id TEXT NOT NULL,
            person TEXT NOT NULL,
            title TEXT,
            source_name TEXT,
            published_at TEXT,
            url TEXT,
            summary TEXT,
            found_at TEXT,
            UNIQUE(provider, external_id)
        )
    """)
    conn.commit()
    conn.close()

def save_item(db_path: str, item: dict) -> bool:
    conn = get_conn(db_path)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO items (
            provider, external_id, person, title, source_name,
            published_at, url, summary, found_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item["provider"],
        item["external_id"],
        item["person"],
        item.get("title", ""),
        item.get("source_name", ""),
        item.get("published_at", ""),
        item.get("url", ""),
        item.get("summary", ""),
        item.get("found_at", ""),
    ))
    inserted = cur.rowcount > 0
    conn.commit()
    conn.close()
    return inserted
