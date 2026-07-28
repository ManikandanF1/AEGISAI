import sqlite3

connection = sqlite3.connect("data/pacds.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS scans(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_time TEXT,
    host TEXT,
    port INTEGER,
    state TEXT,
    service TEXT,
    risk TEXT
)
""")

connection.commit()

print("Database Created Successfully")

connection.close()