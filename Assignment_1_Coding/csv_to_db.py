"""Problem 3: read users from a CSV file and insert them into SQLite."""
import csv
import sqlite3

CSV_FILE = "Assignment_1_Coding/users.csv"
DB_FILE = "users.db"


def main():
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               email TEXT NOT NULL UNIQUE)"""
    )
    inserted = skipped = 0
    with open(CSV_FILE, newline="", encoding="utf-8") as f, conn:
        for row in csv.DictReader(f):
            name = (row.get("name") or "").strip()
            email = (row.get("email") or "").strip().lower()
            if not name or not email:
                skipped += 1
                continue
            cur = conn.execute("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)", (name, email))
            inserted += cur.rowcount
            skipped += 1 - cur.rowcount
    print(f"Inserted {inserted} users, skipped {skipped} rows.")
    for row in conn.execute("SELECT id, name, email FROM users"):
        print(row)
    conn.close()


if __name__ == "__main__":
    main()