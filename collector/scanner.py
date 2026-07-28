import sys
import nmap

from database.operations import save_scan
from analyzer.risk_engine import get_risk
from analyzer.threat_engine import analyze_threat
from collector.asset_info import get_asset_info

# ==========================================================
# AEGISAI - Autonomous Cyber Defense Platform
# Network Scanner
# ==========================================================

scanner = nmap.PortScanner()

# ==========================================================
# Target Host
# ==========================================================

if len(sys.argv) > 1:
    target = sys.argv[1]
else:
    target = "127.0.0.1"

print("=" * 60)
print("        AEGISAI AUTONOMOUS CYBER DEFENSE PLATFORM")
print("=" * 60)

# ==========================================================
# Asset Information
# ==========================================================

print("\nCollecting Asset Information...\n")

asset = get_asset_info()

print(f"Hostname : {asset['Hostname']}")
print(f"IP       : {asset['IP']}")
print(f"MAC      : {asset['MAC']}")
print(f"OS       : {asset['OS']}")

print("\n" + "=" * 60)
print(f"\nScanning Target : {target}\n")

# ==========================================================
# Scan Target
# ==========================================================

try:

    scanner.scan(target, "1-1000")

except Exception as e:

    print(f"\nScan Failed : {e}")
    sys.exit(1)

open_ports = []

for host in scanner.all_hosts():

    print(f"Host : {host}")
    print(f"State: {scanner[host].state()}")

    for protocol in scanner[host].all_protocols():

        print(f"\nProtocol : {protocol}")

        ports = sorted(scanner[host][protocol].keys())

        for port in ports:

            state = scanner[host][protocol][port]["state"]

            service, risk = get_risk(port)

            if state == "open":
                open_ports.append(port)

            print("-" * 40)
            print(f"Port    : {port}")
            print(f"Service : {service}")
            print(f"State   : {state}")
            print(f"Risk    : {risk}")

            save_scan(
                host,
                port,
                state,
                service,
                risk
            )

# ==========================================================
# AI Threat Correlation Engine
# ==========================================================

result = analyze_threat(open_ports)

print("\n" + "=" * 60)
print("          THREAT CORRELATION ENGINE")
print("=" * 60)

print(f"\nAttack Probability : {result['score']}/10")
print(f"Likely Attack      : {result['attack']}")
print(f"MITRE ATT&CK       : {result['mitre']}")

print("\nRecommended Actions")

for recommendation in result["recommendations"]:
    print(f"✔ {recommendation}")

print("\nOpen Ports Summary")

if open_ports:

    for port in open_ports:
        print(f"• {port}")

else:

    print("No Open Ports Found")

print("\n" + "=" * 60)
print("Scan Completed Successfully!")
print("=" * 60)