import pandas as pd

import sqlite3

DB_PATH = "expenses.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            amount_paid REAL
        )
    """)
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
    conn.commit()
    conn.close()


def fetch_expenses() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    return df


def add_expense(date, category, amount, amount_paid=0.0):
    conn = get_connection()
    conn.execute(
    "INSERT INTO expenses (date, category, amount, amount_paid) VALUES (?, ?, ?, ?)",
    (date, category, amount, amount_paid),
    )
    conn.commit()
    conn.close()


def delete_expense(expense_id):
    conn = get_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
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

    

if __name__ == "__main__":
    init_db()
    print(fetch_expenses())




