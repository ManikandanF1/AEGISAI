def generate_alert(service, risk):
    
    if risk == "HIGH":
        return {
            "title": "Critical Security Alert",
            "message": f"High-risk service detected: {service}",
            "level": "HIGH"
        }

    elif risk == "MEDIUM":
        return {
            "title": "Warning",
            "message": f"Medium-risk service detected: {service}",
            "level": "MEDIUM"
        }

    else:
        return {
            "title": "Information",
            "message": f"{service} is running normally",
            "level": "LOW"
        }