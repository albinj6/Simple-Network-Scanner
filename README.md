# 🛡️ Simple Network Scanner

A lightweight, Python-based network utility designed to discover active devices on a local network, identify open ports, and resolve service versions. By leveraging the **Nmap engine** and **Scapy**, it automates the discovery of your local subnet and provides a structured security overview of connected hosts.


## 📖 Description

This tool streamlines the initial phase of network auditing. Instead of manually inputting network parameters, the script automatically detects your active network interface and subnet. It then performs a high-speed scan to identify:
*   **Active Hosts:** Discovers devices using ARP (Address Resolution Protocol) for maximum reliability on local segments.
*   **Hardware Details:** Retrieves MAC addresses and resolves hostnames.
*   **Service Fingerprinting:** Identifies open TCP ports and probes them to determine the specific software and version numbers running on the target.


## ⛔ Pre-requisites

Before running the scanner, ensure your environment meets the following requirements:

### 1. System Dependencies
The core of this scanner is the **Nmap (Network Mapper)** engine. You must install the Nmap binary on your operating system:
*   **Windows:** Download and run the [Nmap Installer](https://nmap.org/download.html).
*   **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install nmap`
*   **macOS:** `brew install nmap`

### 2. Python Libraries
Install the necessary Python wrappers and system utilities via pip: 

`pip install python-nmap scapy psutil`

### 3. Administrative Privileges
Because the script uses raw sockets for ARP discovery (`-PR`) and service fingerprinting, it **must** be run with elevated privileges:
*   **Windows:** Open PowerShell or Command Prompt as **Administrator**.
*   **Linux/macOS:** Run the script using `sudo`.


## 🚀 Usage

1. **Clone the repository:**

    `git clone https://github.com/yourusername/simple-network-scanner.git`
    `cd simple-network-scanner`

2. **Run the scanner:**

   # Linux/macOS
    `sudo python3 scanner.py`

   # Windows (Run terminal as Admin)
    `python scanner.py`

3. **Output:**
   The script will automatically detect your subnet (e.g., `192.168.1.0/24`) and print a formatted table of all discovered devices and their open services.


## ⚠️ Disclaimer
This tool is intended for **educational and ethical security testing purposes only**. Never scan a network or device without explicit authorized permission. The author is not responsible for any misuse or damage caused by this program.