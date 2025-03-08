import subprocess
import socket
import ipaddress
import concurrent.futures
import platform

def parse_ip_range(ip_range):
    """Parse IP range string into a list of IP addresses.
    
    Supports formats:
    - CIDR notation (192.168.1.0/24)
    - Range notation (192.168.1.1-192.168.1.10)
    - Single IP (192.168.1.1)
    """
    if '/' in ip_range:  # CIDR notation
        return [str(ip) for ip in ipaddress.IPv4Network(ip_range, strict=False)]
    elif '-' in ip_range:  # Range notation
        start_ip, end_ip = ip_range.split('-')
        
        # Handle cases where only the last octet is provided in the end IP
        if '.' not in end_ip:
            base = start_ip.rsplit('.', 1)[0]
            end_ip = f"{base}.{end_ip}"
            
        # Convert to integer representation
        start_int = int(ipaddress.IPv4Address(start_ip))
        end_int = int(ipaddress.IPv4Address(end_ip))
        
        return [str(ipaddress.IPv4Address(ip)) for ip in range(start_int, end_int + 1)]
    else:  # Single IP
        return [ip_range]

def is_host_active_icmp(ip, timeout=1):
    """Check if host is active using ICMP ping."""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-w', str(int(timeout * 1000)), ip]
    
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                              universal_newlines=True)
        return result.returncode == 0
    except Exception:
        return False

def is_host_active_tcp(ip, timeout=1):
    """Check if host is active using TCP connection to common ports."""
    common_ports = [80, 443, 22, 21]
    for port in common_ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex((ip, port))
                if result == 0:
                    return True
        except:
            pass
    return False

def check_host(ip, timeout, verbose):
    """Check if a host is active using multiple methods."""
    if verbose:
        print(f"  [-] Checking {ip}...")
        
    # Try ICMP first, then TCP if ICMP fails
    if is_host_active_icmp(ip, timeout):
        if verbose:
            print(f"  [+] Host {ip} is active (ICMP)")
        return ip
    elif is_host_active_tcp(ip, timeout):
        if verbose:
            print(f"  [+] Host {ip} is active (TCP)")
        return ip
    
    return None

def scan_ip_range(ip_range, timeout=1, max_threads=10, verbose=False):
    """Scan IP range for active hosts using parallel processing."""
    try:
        ip_addresses = parse_ip_range(ip_range)
        active_hosts = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            future_to_ip = {executor.submit(check_host, ip, timeout, verbose): ip for ip in ip_addresses}
            
            for future in concurrent.futures.as_completed(future_to_ip):
                result = future.result()
                if result:
                    active_hosts.append(result)
        
        return active_hosts
    except Exception as e:
        print(f"[!] Error scanning IP range: {e}")
        return []
