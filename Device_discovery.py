import nmap
import sys
import socket
import psutil
import ipaddress
from scapy.all import conf, get_if_addr

def get_local_subnet():
    # Detects local subnet by matching the active local IP.
    try:
        local_ip = get_if_addr(conf.iface)
        interfaces = psutil.net_if_addrs()
        for iface_name, addresses in interfaces.items():
            for addr in addresses:
                if addr.family == socket.AF_INET and addr.address == local_ip:
                    netmask = addr.netmask
                    network = ipaddress.IPv4Network(f"{local_ip}/{netmask}", strict=False)
                    return str(network)
        return None
    except Exception as e:
        print(f"[-] Auto-detection failed: {e}")
        return None

def nmap_network_scanner(target_range):
    # Uses the Nmap engine to discover hosts and services efficiently.
    nm = nmap.PortScanner()
    
    print(f"[*] Nmap is scanning {target_range}...")
    print(f"[*] This may take a moment depending on the number of devices...")

    # Nmap Arguments:
    # -sV: Service/Version detection
    # -T4: Faster timing
    # -PR: ARP discovery (best for local networks)
    scan_args = '-sV -T4 -PR'
    
    try:
        nm.scan(hosts=target_range, arguments=scan_args)
    except Exception as e:
        print(f"[-] Nmap error: {e}")
        return

    for host in nm.all_hosts():
        hostname = nm[host].hostname() or "Unknown"
        mac = nm[host]['addresses'].get('mac', 'N/A')
        
        print("\n{:<15} {:<17} {:<20}".format("IP Address", "MAC Address", "Hostname"))
        print("-" * 55)
        print("{:<15} {:<17} {:<20}".format(host, mac, hostname))

        if 'tcp' in nm[host]:
            print(f"\n✅ Scan Results for {host}:")
            print("{:<12} {:<10} {:<30}".format("PORT", "STATUS", "SERVICE/VERSION"))
            print("-" * 65)

            for port in sorted(nm[host]['tcp'].keys()):
                port_data = nm[host]['tcp'][port]
                state = port_data['state']
                
                # Construct a clean version string from Nmap's data
                product = port_data.get('product', '')
                version = port_data.get('version', '')
                extrainfo = port_data.get('extrainfo', '')
                service_info = f"{product} {version} {extrainfo}".strip() or "Unknown Service"
                
                print("{:<12} {:<10} {:<30}".format(f"{port}/tcp", state, service_info))

        else:
            print(f"\n❌ No open ports found on {host}.")

if __name__ == "__main__":
    # Ensure nmap is installed on the system
    # Run as sudo/administrator for ARP and Version scanning
    
    target_range = get_local_subnet()
    
    if not target_range:
        print("[-] Please enter your details manually. You can find your local IP and subnet mask by running ipconfig (Windows) or ifconfig (Mac/Linux) in your terminal.")
        local_ip = input("Enter local IP address (e.g., 192.168.1.14): ")
        subnet_mask = input("Enter subnet mask (e.g., 255.255.255.0): ")
        target_range = f"{local_ip}/{subnet_mask}"

    nmap_network_scanner(target_range)