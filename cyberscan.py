#!/usr/bin/env python3

import argparse
import sys
import time
from modules.ip_scanner import scan_ip_range
from modules.port_scanner import scan_ports
from modules.service_identifier import identify_services
from modules.report_generator import generate_report, save_report

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="CyberScan - Network Reconnaissance Tool",
        epilog="For educational and ethical testing purposes only. Do not use against unauthorized systems."
    )
    
    parser.add_argument("-i", "--ip", required=True, 
                        help="IP address range to scan (e.g., 192.168.1.1-192.168.1.10 or 192.168.1.0/24)")
    parser.add_argument("-p", "--ports", default="1-1024",
                        help="Port range to scan (e.g., 80,443,8080 or 1-1024)")
    parser.add_argument("-t", "--timeout", type=float, default=1.0,
                        help="Timeout for connections in seconds")
    parser.add_argument("-o", "--output", 
                        help="Output file to save results (will be saved in CSV format)")
    parser.add_argument("--threads", type=int, default=10,
                        help="Number of threads for parallel scanning")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose output")
    
    return parser.parse_args()

def display_banner():
    """Display tool banner."""
    banner = """
    ╔═══════════════════════════════════════════╗
    ║               CyberScan                   ║
    ║        Network Reconnaissance Tool        ║
    ║                                           ║
    ║                 BY RAD50                  ║
    ╚═══════════════════════════════════════════╝
    """
    print(banner)
    
def main():
    """Main function to run the tool."""
    # Display banner
    display_banner()
    
    # Parse command-line arguments
    args = parse_arguments()
    
    print("[+] Starting CyberScan...")
    start_time = time.time()
    
    try:
        # Step 1: Scan IP range for active hosts
        print(f"[+] Scanning IP range: {args.ip}")
        active_hosts = scan_ip_range(args.ip, args.timeout, args.threads, args.verbose)
        
        if not active_hosts:
            print("[-] No active hosts found.")
            return
        
        print(f"[+] Found {len(active_hosts)} active hosts")
        
        # Step 2 & 3: Scan ports and identify services for each active host
        results = []
        for host in active_hosts:
            print(f"[+] Scanning ports on {host}")
            open_ports = scan_ports(host, args.ports, args.timeout, args.threads, args.verbose)
            
            if not open_ports:
                print(f"[-] No open ports found on {host}")
                continue
            
            print(f"[+] Found {len(open_ports)} open ports on {host}")
            
            # Identify services on open ports
            print(f"[+] Identifying services on {host}")
            host_services = identify_services(host, open_ports, args.timeout, args.verbose)
            
            results.append({
                "host": host,
                "open_ports": open_ports,
                "services": host_services
            })
        
        # Step 4: Generate and display report
        if results:
            report = generate_report(results)
            
            if args.output:
                save_report(report, args.output)
                print(f"[+] Results saved to {args.output}")
    
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
    except Exception as e:
        print(f"[!] Error: {e}")
    
    print(f"[+] Scan completed in {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
