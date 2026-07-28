HIGH_RISK_PORTS = {
    21: ("FTP", "Disable FTP if not required and use SFTP instead."),
    23: ("Telnet", "Disable Telnet and use SSH for secure remote access."),
    25: ("SMTP", "Monitor mail server activity and restrict unauthorized access."),
    135: ("RPC", "Verify RPC exposure and restrict unnecessary remote access."),
    139: ("NetBIOS", "Disable NetBIOS if not required."),
    445: ("SMB", "Monitor SMB traffic and ensure the latest security patches are installed."),
    3389: ("RDP", "Restrict RDP access using VPN and Multi-Factor Authentication.")
}

MEDIUM_RISK_PORTS = {
    22: ("SSH", "Allow only trusted IP addresses and use key-based authentication."),
    80: ("HTTP", "Redirect HTTP traffic to HTTPS whenever possible."),
    110: ("POP3", "Use encrypted email protocols."),
    143: ("IMAP", "Enable SSL/TLS for IMAP communication."),
    443: ("HTTPS", "Keep SSL/TLS certificates updated.")
}


def get_risk(port):

    if port in HIGH_RISK_PORTS:
        service, recommendation = HIGH_RISK_PORTS[port]
        return service, "HIGH", recommendation

    elif port in MEDIUM_RISK_PORTS:
        service, recommendation = MEDIUM_RISK_PORTS[port]
        return service, "MEDIUM", recommendation

    else:
        return "Unknown", "LOW", "No immediate action required."