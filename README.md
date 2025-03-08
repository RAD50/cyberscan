
```markdown
# 🔍 CyberScan - Network Reconnaissance Tool

CyberScan is a Python-powered network scanning tool designed for ethical hacking and penetration
testing. It helps identify active hosts, open ports, and running services to uncover potential vulnerabilities.

# ⚠️ Legal Disclaimer

> This tool is for EDUCATIONAL USE ONLY.  
> Unauthorized scanning of networks/systems is illegal. Always obtain explicit written permission
 before using CyberScan on any network you don't own or manage. Developers assume no liability for misuse.

# ✨ Key Features

- Smart IP Scanning  
  Detect active hosts using ICMP pings + TCP checks (supports CIDR, IP ranges, and single IPs)
- Port Range Analysis  
  Scan 1-65535 ports with customizable ranges
- Service Fingerprinting  
  Identify 100+ services via port numbers + banner grabbing
- Multi-Threaded Scans  
  Accelerate scans with configurable threads
- Detailed Reporting  
  Export results to TXT, CSV, or JSON formats

# 🛠️ Installation

Requirements: Python 3.6+

``` bash
git clone https://github.com/yourusername/CyberScan.git
cd CyberScan
chmod +x cyberscan.py  # Make executable (optional)
```

 🚀 Basic Usage

```
# Scan single host
python cyberscan.py -i 192.168.1.1

# Scan subnet with CSV output
python cyberscan.py -i 10.0.0.0/24 -p 1-5000 -o results.csv
```

# 🔧 Full Command Options

| Option          | Description                                  | Default     |
|-----------------|----------------------------------------------|-------------|
| `-i, --ip`      | IP range (Required)                         | -           |
| `-p, --ports`   | Ports to scan (e.g., `80,443` or `1-1024`)  | 1-1024      |
| `-t, --timeout` | Connection timeout (seconds)                | 1.0         |
| `-o, --output`  | Save results (.txt/.csv/.json)              | -           |
| `--threads`     | Parallel threads                            | 10          |
| `-v, --verbose` | Show detailed progress                      | Off         |

 🧠 How It Works

1. Host Discovery
   - Hybrid detection (ICMP + TCP)
   - Supports CIDR, IP ranges, single IPs

2. Port Scanning
   - TCP Connect Scan method
   - Customizable port ranges

3. Service Identification
   - Banner grabbing + port database
   - 75+ predefined service mappings

4. Reporting
   - Console output with service details
   - File export in multiple formats

Sample Output:
```
============================================================
CYBERSCAN REPORT - 2023-08-20 14:30:00
============================================================

Host: 192.168.1.1
----------------------------------------
Open ports:
  22/tcp: SSH
  80/tcp: HTTP
  443/tcp: HTTPS

Service Banners:
  Port 22: SSH-2.0-OpenSSH_8.2p1
  Port 80: HTTP/1.1 200 OK...
```

 🌟 Advanced Usage

```bash
# Scan IP range with aggressive timing
python cyberscan.py -i 192.168.1.1-192.168.1.50 -t 0.5 --threads 20

# Full port scan with JSON output
python cyberscan.py -i 10.0.0.5 -p 1-65535 -v -o full_scan.json
```

 ⚠️ Limitations

- May require root privileges for ICMP scans
- Firewalls may block detection attempts
- Service banners can be hidden/obfuscated

 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Submit Pull Request

 📜 License

MIT License - See [LICENSE](LICENSE) for details.
```
