from flask import Flask, render_template, redirect, request, send_file
import sqlite3
import os
import subprocess
import sys

from reports.report import generate_pdf
from reports.export_csv import generate_csv

# ==========================================================
# AEGISAI - Autonomous Cyber Defense Platform
# Flask Application
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE = os.path.join(BASE_DIR, "data", "pacds.db")

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# ==========================================================
# DATABASE
# ==========================================================

def get_scan_results(search=""):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    if search == "":

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

    else:

        cursor.execute("""
            SELECT
                scan_time,
                host,
                port,
                state,
                service,
                risk
            FROM scans
            WHERE
                host LIKE ?
                OR CAST(port AS TEXT) LIKE ?
                OR service LIKE ?
                OR risk LIKE ?
            ORDER BY id DESC
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))

    rows = cursor.fetchall()

    connection.close()

    return rows


# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/dashboard")
def dashboard():

    search = request.args.get("search", "")

    scans = get_scan_results(search)

    total_assets = len(set(row[1] for row in scans))

    high_risk = sum(1 for row in scans if row[5] == "HIGH")
    medium_risk = sum(1 for row in scans if row[5] == "MEDIUM")
    low_risk = sum(1 for row in scans if row[5] == "LOW")

    latest_scan = scans[0][0] if scans else "No Scan"

    total = high_risk + medium_risk + low_risk

    if total == 0:
        threat_score = 0
    else:
        score = (high_risk * 3) + (medium_risk * 2) + low_risk
        threat_score = round((score / (total * 3)) * 10, 1)

    if high_risk >= 3:

        ai_attack = "Possible Lateral Movement"

        mitre = "T1021 - Remote Services"

    elif medium_risk >= 3:

        ai_attack = "Possible Reconnaissance"

        mitre = "T1595 - Active Scanning"

    else:

        ai_attack = "No Immediate Threat"

        mitre = "None"

    recommendations = [

        "Restrict SMB Access",
        "Enable Windows Firewall",
        "Monitor RPC Connections",
        "Apply Latest Security Updates"

    ]

    return render_template(

        "index.html",

        scans=scans,

        total_assets=total_assets,

        high_risk=high_risk,

        medium_risk=medium_risk,

        low_risk=low_risk,

        latest_scan=latest_scan,

        threat_score=threat_score,

        ai_attack=ai_attack,

        mitre=mitre,

        recommendations=recommendations,

        search=search

    )


# ==========================================================
# ASSETS PAGE
# ==========================================================

@app.route("/assets")
def assets():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            host,
            port,
            service,
            risk
        FROM scans
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    assets = []

    seen = set()

    for row in rows:

        key = (row[0], row[1])

        if key not in seen:

            seen.add(key)

            assets.append((
                row[0],      # Host
                row[0],      # IP/Host
                row[1],      # Port
                row[2],      # Service
                row[3]       # Risk
            ))

    return render_template(
        "assets.html",
        assets=assets
    )


# ==========================================================
# THREATS PAGE
# ==========================================================

@app.route("/threats")
def threats():

    threats = [

        {
            "attack": "Lateral Movement",
            "mitre": "T1021",
            "severity": "HIGH"
        },

        {
            "attack": "Port Scan",
            "mitre": "T1595",
            "severity": "MEDIUM"
        },

        {
            "attack": "Normal Activity",
            "mitre": "-",
            "severity": "LOW"
        }

    ]

    return render_template(
        "threats.html",
        threats=threats
    )


# ==========================================================
# REPORTS PAGE
# ==========================================================

@app.route("/reports")
def reports():

    return render_template("reports.html")


# ==========================================================
# SETTINGS PAGE
# ==========================================================

@app.route("/settings")
def settings():

    return render_template("settings.html")


# ==========================================================
# NETWORK SCAN
# ==========================================================

@app.route("/scan", methods=["POST"])
def scan():

    target = request.form.get("target")

    if not target:
        target = "127.0.0.1"

    subprocess.run(
        [
            sys.executable,
            "-m",
            "collector.scanner",
            target
        ],
        cwd=BASE_DIR
    )

    return redirect("/")


# ==========================================================
# EXPORT PDF
# ==========================================================

@app.route("/export")
def export_pdf():

    pdf_file = generate_pdf()

    return send_file(
        pdf_file,
        as_attachment=True
    )


# ==========================================================
# EXPORT CSV
# ==========================================================

@app.route("/export_csv")
def export_csv():

    csv_file = generate_csv()

    return send_file(
        csv_file,
        as_attachment=True
    )


# ==========================================================
# START SERVER
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )