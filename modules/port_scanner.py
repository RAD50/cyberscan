import socket
import concurrent.futures
import time

def parse_port_range(port_range):
    """Parse port range string into a list of ports.
    
    Supports formats:
    - Range notation (1-1024)
    - Comma-separated list (80,443,8080)
    - Single port (80)
    """
    ports = []
    
    if ',' in port_range:
        # Handle comma-separated list
        for part in port_range.split(','):
            if '-' in part:
                # Handle ranges within comma-separated list
                start, end = map(int, part.split('-'))
                ports.extend(range(start, end + 1))
            else:
                # Handle single port
                ports.append(int(part))
    elif '-' in port_range:
        # Handle simple range
        start, end = map(int, port_range.split('-'))
        ports = list(range(start, end + 1))
    else:
        # Handle single port
        ports = [int(port_range)]
        
    return ports

def check_port(host, port, timeout):
    """Check if a specific port is open on a host."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            return port if result == 0 else None
    except:
        return None

def scan_ports(host, port_range="1-1024", timeout=1, max_threads=100, verbose=False):
    """Scan ports on a specific host using parallel processing."""
    try:
        ports = parse_port_range(port_range)
        open_ports = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            future_to_port = {executor.submit(check_port, host, port, timeout): port for port in ports}
            
            for future in concurrent.futures.as_completed(future_to_port):
                port = future_to_port[future]
                result = future.result()
                
                if result:
                    if verbose:
                        print(f"  [+] Port {port} is open on {host}")
                    open_ports.append(port)
        
        return sorted(open_ports)
    except Exception as e:
        print(f"[!] Error scanning ports on {host}: {e}")
        return []
