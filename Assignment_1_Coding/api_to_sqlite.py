"""Problem 1: fetch books from a REST API, store them in SQLite, display them."""
import sqlite3
import requests

API_URL = "https://openlibrary.org/search.json"
DB_FILE = "books.db"


def fetch_books():
    params = {"q": "python", "limit": 10, "fields": "title,author_name,first_publish_year"}
    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()
    books = []
    for item in response.json().get("docs", []):
        title = item.get("title", "Unknown")
        authors = item.get("author_name") or ["Unknown"]
        year = item.get("first_publish_year")
        books.append((title, authors[0], year))
    return books


def save_books(books):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS books (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT NOT NULL,
               author TEXT,
               year INTEGER,
               UNIQUE(title, author))"""
    )
    before = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    with conn:
        conn.executemany("INSERT OR IGNORE INTO books (title, author, year) VALUES (?, ?, ?)", books)
    after = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    conn.close()
    return after - before


def show_books():
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute("SELECT id, title, author, year FROM books").fetchall()
    conn.close()
    print(f"{'ID':<4}{'Title':<45}{'Author':<28}{'Year'}")
    for id_, title, author, year in rows:
        print(f"{id_:<4}{title[:43]:<45}{author[:26]:<28}{year or ''}")


if __name__ == "__main__":
    try:
        books = fetch_books()
    except requests.RequestException as err:
        print("Could not fetch data from the API:", err)
        raise SystemExit(1)
    new_rows = save_books(books)
    print(f"Fetched {len(books)} books, saved {new_rows} new rows.\n")
    show_books()