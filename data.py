import pandas as pd

import sqlite3

DB_PATH = "expenses.db"

PERSON_COLORS = {"Paul": "#3B82F6", "Camila": "#EC4899"}
PERSON_LIGHT_COLORS = {"Paul": "#DBEAFE", "Camila": "#FCE7F3"}

def format_timestamp(ts):
    dt = pd.to_datetime(ts)
    hour12 = dt.strftime("%I").lstrip("0") or "12"
    ampm = dt.strftime("%p").lower()
    return f"{dt.month}-{dt.day} {hour12}:{dt.strftime('%M')}{ampm}"

def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            description TEXT,
            amount REAL,
            amount_paid REAL
        )
    """)
    try:
        conn.execute("ALTER TABLE expenses RENAME COLUMN category TO description")
    except sqlite3.OperationalError:
        pass
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            end_date TEXT,
            title TEXT,
            person TEXT
        )
    """)
    try:
        conn.execute("ALTER TABLE events ADD COLUMN end_date TEXT")
    except sqlite3.OperationalError:
        pass
    conn.execute("""
        CREATE TABLE IF NOT EXISTS grocery_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT,
            person TEXT,
            store TEXT,
            checked INTEGER DEFAULT 0
        )
    """)
    try:
        conn.execute("ALTER TABLE grocery_items ADD COLUMN store TEXT")
    except sqlite3.OperationalError:
        pass
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            person TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def fetch_expenses() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    return df


def add_expense(date, description, amount, amount_paid=0.0):
    conn = get_connection()
    conn.execute(
    "INSERT INTO expenses (date, description, amount, amount_paid) VALUES (?, ?, ?, ?)",
    (date, description, amount, amount_paid),
    )
    conn.commit()
    conn.close()


def delete_expense(expense_id):
    conn = get_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()


def clear_expenses():
    conn = get_connection()
    conn.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()


def update_expense(expense_id, amount, amount_paid):
     conn = get_connection()
     conn.execute(
        "UPDATE expenses SET amount = ?, amount_paid = ? WHERE id = ?",
        (amount, amount_paid, expense_id),
    )
     conn.commit()
     conn.close()

def fetch_events() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM events", conn)
    conn.close()
    return df

def add_event(date, title, person, end_date=None):
    conn = get_connection()
    conn.execute(
        "INSERT INTO events (date, end_date, title, person) VALUES (?, ?, ?, ?)",
        (date, end_date or date, title, person),
    )
    conn.commit()
    conn.close()

def delete_event(event_id):
    conn = get_connection()
    conn.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

def update_event(event_id, date, title, person, end_date=None):
    conn = get_connection()
    conn.execute(
        "UPDATE events SET date = ?, end_date = ?, title = ?, person = ? WHERE id = ?",
        (date, end_date or date, title, person, event_id),
    )
    conn.commit()
    conn.close()

def fetch_grocery_items() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM grocery_items", conn)
    conn.close()
    return df

def add_grocery_item(item, person, store):
    conn = get_connection()
    conn.execute(
        "INSERT INTO grocery_items (item, person, store, checked) VALUES (?, ?, ?, 0)",
        (item, person, store),
    )
    conn.commit()
    conn.close()

def delete_grocery_item(item_id):
    conn = get_connection()
    conn.execute("DELETE FROM grocery_items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def toggle_grocery_item(item_id, checked):
    conn = get_connection()
    conn.execute("UPDATE grocery_items SET checked = ? WHERE id = ?", (int(checked), item_id))
    conn.commit()
    conn.close()


def fetch_notes() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM notes", conn)
    conn.close()
    return df

def add_note(text, person, created_at):
    conn = get_connection()
    conn.execute(
        "INSERT INTO notes (text, person, created_at) VALUES (?, ?, ?)",
        (text, person, created_at),
    )
    conn.commit()
    conn.close()

def delete_note(note_id):
    conn = get_connection()
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(fetch_expenses())




