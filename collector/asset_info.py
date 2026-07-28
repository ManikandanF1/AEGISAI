import socket
import platform
import uuid


def get_asset_info():

    hostname = socket.gethostname()

    ip_address = socket.gethostbyname(hostname)

    mac = ':'.join(("%012X" % uuid.getnode())[i:i+2] for i in range(0, 12, 2))

    operating_system = platform.system() + " " + platform.release()

    return {
        "Hostname": hostname,
        "IP": ip_address,
        "MAC": mac,
        "OS": operating_system
    }