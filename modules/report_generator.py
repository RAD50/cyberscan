import csv
import json
import os
from datetime import datetime

def generate_report(results):
    """Generate a structured report from scan results."""
    report = {
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_hosts": len(results),
        "hosts": results
    }
    
    # Print formatted report to console
    print("\n" + "="*60)
    print(f"CYBERSCAN REPORT - {report['scan_time']}")
    print("="*60)
    
    for host_data in results:
        host = host_data['host']
        open_ports = host_data['open_ports']
        services = host_data['services']
        
        print(f"\nHost: {host}")
        print("-" * 40)
        
        if not open_ports:
            print("No open ports found.")
            continue
            
        print("Open ports:")
        for port in open_ports:
            service_info = services.get(port, {})
            service_name = service_info.get('name', 'unknown')
            print(f"  {port}/tcp: {service_name}")
            
        print("\nDetailed service information:")
        for port in open_ports:
            service_info = services.get(port, {})
            banner = service_info.get('banner', 'No banner')
            # Truncate banner if it's too long
            if len(banner) > 80:
                banner = banner[:77] + "..."
            print(f"  Port {port}: {banner}")
    
    print("\n" + "="*60 + "\n")
    
    return report

def save_report(report, output_file):
    """Save the report to a file."""
    file_extension = os.path.splitext(output_file)[1].lower()
    
    try:
        if file_extension == '.json':
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
        elif file_extension == '.csv':
            with open(output_file, 'w', newline='') as f:
                csv_writer = csv.writer(f)
                
                # Write header
                csv_writer.writerow(['Host', 'Port', 'Service', 'Banner'])
                
                # Write data
                for host_data in report['hosts']:
                    host = host_data['host']
                    services = host_data['services']
                    
                    for port, service_info in services.items():
                        csv_writer.writerow([
                            host,
                            port,
                            service_info.get('name', 'unknown'),
                            service_info.get('banner', 'No banner')
                        ])
        else:
            # Default to text format
            with open(output_file, 'w') as f:
                f.write(f"CYBERSCAN REPORT - {report['scan_time']}\n")
                f.write("="*60 + "\n\n")
                
                for host_data in report['hosts']:
                    host = host_data['host']
                    open_ports = host_data['open_ports']
                    services = host_data['services']
                    
                    f.write(f"Host: {host}\n")
                    f.write("-" * 40 + "\n")
                    
                    if not open_ports:
                        f.write("No open ports found.\n")
                        continue
                        
                    f.write("Open ports:\n")
                    for port in open_ports:
                        service_info = services.get(port, {})
                        service_name = service_info.get('name', 'unknown')
                        f.write(f"  {port}/tcp: {service_name}\n")
                    
                    f.write("\nDetailed service information:\n")
                    for port in open_ports:
                        service_info = services.get(port, {})
                        banner = service_info.get('banner', 'No banner')
                        if len(banner) > 80:
                            banner = banner[:77] + "..."
                        f.write(f"  Port {port}: {banner}\n")
                    
                    f.write("\n" + "="*60 + "\n")
        
        return True
    except Exception as e:
        print(f"[!] Error saving report: {e}")
        return False
