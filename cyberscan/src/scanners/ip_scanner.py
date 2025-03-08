class IPScanner:
    def __init__(self, ip_range):
        self.ip_range = ip_range
        self.active_hosts = []

    def scan(self):
        # Implement the logic to scan the IP range for active hosts
        pass

    def is_host_active(self, ip):
        # Implement the logic to check if a host is active using ICMP echo requests
        pass

    def get_active_hosts(self):
        return self.active_hosts