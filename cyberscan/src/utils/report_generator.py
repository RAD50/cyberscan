def generate_report(scan_results, output_format='text', filename='scan_report'):
    if output_format == 'text':
        with open(f"{filename}.txt", 'w') as f:
            for host, details in scan_results.items():
                f.write(f"Active Host: {host}\n")
                f.write(f"Open Ports: {', '.join(map(str, details['open_ports']))}\n")
                f.write(f"Services: {', '.join(details['services'])}\n\n")
    elif output_format == 'csv':
        import csv
        with open(f"{filename}.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Active Host', 'Open Ports', 'Services'])
            for host, details in scan_results.items():
                writer.writerow([host, ', '.join(map(str, details['open_ports'])), ', '.join(details['services'])])
    else:
        raise ValueError("Unsupported output format. Use 'text' or 'csv'.")