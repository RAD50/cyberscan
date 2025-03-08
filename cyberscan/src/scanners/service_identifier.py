class ServiceIdentifier:
    def __init__(self, banner_database):
        self.banner_database = banner_database

    def identify_service(self, port, banner):
        """
        Identifies the service based on the provided port and banner.
        """
        service_name = self.banner_database.get(banner, "Unknown Service")
        return service_name

    def get_banner(self, socket):
        """
        Retrieves the service banner from the given socket connection.
        """
        try:
            socket.settimeout(2)
            banner = socket.recv(1024).decode('utf-8').strip()
            return banner
        except Exception as e:
            return None

    def identify_services(self, open_ports):
        """
        Identifies services for a list of open ports.
        """
        services = {}
        for port in open_ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', port))  # Replace 'localhost' with the target IP
                banner = self.get_banner(s)
                if banner:
                    service_name = self.identify_service(port, banner)
                    services[port] = service_name
        return services