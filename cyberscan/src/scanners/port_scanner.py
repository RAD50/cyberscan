class PortScanner:
    def __init__(self, ip_address, port_range):
        self.ip_address = ip_address
        self.port_range = port_range

    def scan_ports(self):
        open_ports = []
        for port in self.port_range:
            if self.is_port_open(port):
                open_ports.append(port)
        return open_ports

    def is_port_open(self, port):
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set a timeout for the connection attempt
        result = sock.connect_ex((self.ip_address, port))
        sock.close()
        return result == 0