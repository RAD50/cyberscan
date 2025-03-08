import socket
import re
from .constants import PORT_TO_SERVICE, BANNER_PATTERNS

def get_banner(host, port, timeout=1):
    """Attempt to retrieve the service banner from a specified port."""
    banner = ""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            
            # Some common protocols require initial data to prompt a response
            if port == 80 or port == 443:
                s.send(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
            elif port == 21 or port == 22 or port == 25 or port == 110:
                pass  # These protocols typically send a banner upon connection
            else:
                s.send(b"\r\n")
                
            # Try to receive data
            try:
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            except socket.timeout:
                pass
    except Exception:
        pass
        
    return banner

def identify_service_from_banner(banner):
    """Identify service based on banner content."""
    if not banner:
        return None
    
    # Check for pattern matches in the banner
    for pattern, service in BANNER_PATTERNS.items():
        if re.search(pattern, banner, re.IGNORECASE):
            return service
    
    return None

def identify_service_from_port(port):
    """Identify service based on well-known port numbers."""
    return PORT_TO_SERVICE.get(port, f"unknown-{port}")

def identify_services(host, open_ports, timeout=1, verbose=False):
    """Identify services running on open ports."""
    services = {}
    
    for port in open_ports:
        if verbose:
            print(f"  [-] Getting banner for {host}:{port}")
            
        banner = get_banner(host, port, timeout)
        
        if banner and verbose:
            # Print only first 50 chars of banner if verbose
            print(f"  [-] Banner: {banner[:50]}...")
            
        service = identify_service_from_banner(banner)
        
        if not service:
            service = identify_service_from_port(port)
            
        services[port] = {
            "name": service,
            "banner": banner if banner else "No banner received"
        }
        
        if verbose:
            print(f"  [+] Service on {port}: {service}")
    
    return services
