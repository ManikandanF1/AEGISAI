import sqlite3

connection = sqlite3.connect("data/pacds.db")

cursor = connection.cursor()

cursor.execute("SELECT * FROM scans")

rows = cursor.fetchall()

print("\n========== SCAN RESULTS ==========\n")

for row in rows:
    print(row)

connection.close()