import sqlite3
import csv
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE = os.path.join(BASE_DIR, "data", "pacds.db")

REPORT_FOLDER = os.path.join(BASE_DIR, "reports")


def generate_csv():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            scan_time,
            host,
            port,
            state,
            service,
            risk
        FROM scans
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    filename = "AEGISAI_Report_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"

    filepath = os.path.join(REPORT_FOLDER, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Scan Time",
            "Host",
            "Port",
            "State",
            "Service",
            "Risk"
        ])

        writer.writerows(rows)

    print("CSV Report Generated Successfully!")

    return filepath


if __name__ == "__main__":

    path = generate_csv()

    print(path)