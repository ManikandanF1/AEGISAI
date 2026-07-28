from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE = os.path.join(BASE_DIR, "data", "pacds.db")

REPORTS_DIR = os.path.join(BASE_DIR, "reports")


def generate_pdf():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT scan_time,
               host,
               port,
               state,
               service,
               risk
        FROM scans
        ORDER BY id DESC
    """)

    scans = cursor.fetchall()

    connection.close()

    filename = os.path.join(
        REPORTS_DIR,
        f"AEGISAI_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>AEGISAI INCIDENT REPORT</b>", styles["Title"]))
    elements.append(Paragraph(f"Generated: {datetime.now()}", styles["Normal"]))
    elements.append(Paragraph("<br/>", styles["Normal"]))

    data = [
        ["Time", "Host", "Port", "State", "Service", "Risk"]
    ]

    high = 0
    medium = 0
    low = 0

    for row in scans:

        data.append(list(row))

        if row[5] == "HIGH":
            high += 1
        elif row[5] == "MEDIUM":
            medium += 1
        else:
            low += 1

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,0), colors.darkblue),

        ("TEXTCOLOR", (0,0), (-1,0), colors.white),

        ("GRID", (0,0), (-1,-1), 1, colors.black),

        ("BACKGROUND", (0,1), (-1,-1), colors.beige),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("BOTTOMPADDING",(0,0),(-1,0),10),

    ]))

    elements.append(table)

    elements.append(Paragraph("<br/>", styles["Normal"]))

    elements.append(
        Paragraph(
            f"<b>High Risk:</b> {high}<br/>"
            f"<b>Medium Risk:</b> {medium}<br/>"
            f"<b>Low Risk:</b> {low}",
            styles["Normal"]
        )
    )

    doc.build(elements)

    return filename


if __name__ == "__main__":

    path = generate_pdf()

    print("PDF Report Generated Successfully!")

    print(path)