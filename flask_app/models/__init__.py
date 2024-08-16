import sqlite3

# manage database connections
def get_db_connection():
    conn = sqlite3.connect("flask_app/insurance.db")
    conn.row_factory = sqlite3.Row
    return conn
