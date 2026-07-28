def analyze_threat(open_ports):
    
    attack = "No Significant Threat"
    mitre = "N/A"
    score = 2.0
    recommendations = []

    # SMB + RPC
    if 445 in open_ports and 135 in open_ports:

        attack = "Possible Lateral Movement"

        mitre = "T1021 - Remote Services"

        score = 9.2

        recommendations = [
            "Restrict SMB Access",
            "Enable Windows Firewall",
            "Monitor RPC Connections",
            "Apply Latest Windows Security Updates"
        ]

    # RDP
    elif 3389 in open_ports:

        attack = "Possible Remote Desktop Attack"

        mitre = "T1110 - Brute Force"

        score = 8.5

        recommendations = [
            "Enable MFA",
            "Limit RDP Access",
            "Use Strong Passwords"
        ]

    return {
        "attack": attack,
        "mitre": mitre,
        "score": score,
        "recommendations": recommendations
    }