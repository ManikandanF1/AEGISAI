import ipaddress
import socket
import subprocess
import platform

# ==========================================================
# AEGISAI Network Discovery
# ==========================================================

def ping(host):

    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "1", "-w", "300", str(host)]
    else:
        command = ["ping", "-c", "1", "-W", "1", str(host)]

    result = subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return result.returncode == 0


def discover_network(network):

    devices = []

    print("=" * 60)
    print("        AEGISAI NETWORK DISCOVERY")
    print("=" * 60)

    for ip in ipaddress.ip_network(network, strict=False).hosts():

        ip = str(ip)

        if ping(ip):

            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except:
                hostname = "Unknown"

            device = {
                "ip": ip,
                "hostname": hostname
            }

            devices.append(device)

            print(f"[+] {ip:<16} {hostname}")

    print("=" * 60)
    print(f"Devices Found : {len(devices)}")
    print("=" * 60)

    return devices


if __name__ == "__main__":

    discover_network("192.168.1.0/24")