import socket

UDP_IP = "172.20.10.4" # The Pi's IP address
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2) # Prevent the script from hanging forever if the Pi is off

def fetch():
    try:
        # 1. Send to Pi
        sock.sendto("Data".encode(), (UDP_IP, UDP_PORT))

        # 2. Wait for Pi to write back
        data, addr = sock.recvfrom(1024)
        return data.decode()
        
    except socket.timeout:
        print("Error: Pi did not respond in time.")
