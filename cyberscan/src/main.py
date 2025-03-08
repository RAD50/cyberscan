import sys
from scanners.ip_scanner import IPScanner
from scanners.port_scanner import PortScanner
from scanners.service_identifier import ServiceIdentifier
from utils.report_generator import generate_report

def main():
    print("Welcome to CyberScan!")
    
    # Get user input for IP range and port range
    ip_range = input("Enter the IP range (e.g., 192.168.1.1-192.168.1.255): ")
    port_range = input("Enter the port range (e.g., 1-1024): ")

    # Initialize scanners
    ip_scanner = IPScanner()
    port_scanner = PortScanner()
    service_identifier = ServiceIdentifier()

    # Scan for active hosts
    active_hosts = ip_scanner.scan(ip_range)
    print(f"Active hosts found: {active_hosts}")

    # Scan for open ports on active hosts
    open_ports = {}
    for host in active_hosts:
        open_ports[host] = port_scanner.scan(host, port_range)
        print(f"Open ports for {host}: {open_ports[host]}")

    # Identify services for open ports
    services = {}
    for host, ports in open_ports.items():
        services[host] = service_identifier.identify(ports)
        print(f"Services for {host}: {services[host]}")

    # Generate report
    generate_report(active_hosts, open_ports, services)

if __name__ == "__main__":
    main()