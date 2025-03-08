# CyberScan - Network Scanner Tool

## Overview
CyberScan is a network scanning tool designed for ethical hacking and penetration testing. It assists in network reconnaissance by identifying active hosts, open ports, and running services, providing critical insights for vulnerability assessment and system security enhancement.

## Features
- **IP Scanning**: Scans a specified range of IP addresses to identify active hosts using ICMP echo requests.
- **Port Scanning**: Scans specified ports on active hosts to identify open ports using TCP connect scans.
- **Service Identification**: Connects to open ports to retrieve service banners and identify services based on those banners.
- **Reporting**: Generates detailed reports of findings, including active hosts, open ports, and identified services, with options to save in various formats.

## Installation
To install the required dependencies, run:
```
pip install -r requirements.txt
```

## Usage
To run the CyberScan tool, execute the following command:
```
python src/main.py
```
Follow the prompts to specify the IP range and port range for scanning.

## Legal and Ethical Use
CyberScan is intended for educational and research purposes only. Ensure you have authorization before scanning any network or system. Unauthorized access to computer systems is illegal and unethical.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.