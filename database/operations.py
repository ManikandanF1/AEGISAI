import sqlite3
from datetime import datetime


def save_scan(host, port, state, service, risk):

    connection = sqlite3.connect("data/pacds.db")

    cursor = connection.cursor()

    scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO scans(scan_time, host, port, state, service, risk)
    VALUES(?,?,?,?,?,?)
    """, (scan_time, host, port, state, service, risk))

    connection.commit()

    connection.close()