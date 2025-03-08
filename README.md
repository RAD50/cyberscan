# CyberScan - Network Reconnaissance Tool

CyberScan is a Python-based network reconnaissance tool developed for educational purposes and ethical hacking practice. It scans networks to identify active hosts, open ports, and running services.

## Disclaimer

**This tool is for EDUCATIONAL PURPOSES ONLY.**

Do not use this tool against any systems or networks without explicit permission from the owner. Unauthorized scanning of networks may violate laws and regulations.

## Features

- IP range scanning using ICMP and TCP methods
- Port scanning with customizable port ranges
- Service identification based on port numbers and banners
- Detailed reporting with options to save results
- Multi-threaded scanning for improved performance

## Requirements

- Python 3.6 or higher
- No external dependencies (uses built-in Python libraries)

## Installation

1. Clone the repository or download the source code
2. No additional installation steps required

## Usage

```bash
python cyberscan.py -i <IP_RANGE> [OPTIONS]
```

### Examples

Scan a single host for common ports:
```bash
python cyberscan.py -i 192.168.1.1
```

Scan a range of IP addresses:
```bash
python cyberscan.py -i 192.168.1.1-192.168.1.10
```

Scan a subnet using CIDR notation:
```bash
python cyberscan.py -i 192.168.1.0/24
```

Scan specific ports:
```bash
python cyberscan.py -i 192.168.1.1 -p 80,443,8080
```

Scan a port range:
```bash
python cyberscan.py -i 192.168.1.1 -p 1-1024
```

Save results to a file:
```bash
python cyberscan.py -i 192.168.1.1 -o results.csv
```

### Command Line Options

- `-i, --ip`: IP address range to scan (required)
- `-p, --ports`: Port range to scan (default: 1-1024)
- `-t, --timeout`: Connection timeout in seconds (default: 1.0)
- `-o, --output`: Output file to save results
- `--threads`: Number of threads for parallel scanning (default: 10)
- `-v, --verbose`: Enable verbose output

## Technical Details

CyberScan uses several techniques for network reconnaissance:

1. **IP Scanning**: Uses ICMP ping and TCP connection attempts to identify active hosts
2. **Port Scanning**: Uses TCP connect scan to identify open ports
3. **Service Identification**: Uses banner grabbing and known port mappings to identify services
4. **Multi-threading**: Uses Python's concurrent.futures for parallel scanning

## Limitations

- ICMP scanning may require administrator/root privileges
- Scanning large networks may take significant time
- Banner grabbing may not identify all services correctly
- Some networks may have firewalls that block scanning attempts

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
