from scapy.all import srp, Ether, ARP
import sys

def arp_scan(target_ip_range):
    """
    Performs an ARP scan on the specified IP range.
    """
    print(f"[*] Scanning for devices on {target_ip_range}...")

    # 1. Create the Ether frame
    # We set the destination MAC (dst) to 'ff:ff:ff:ff:ff:ff' (broadcast)
    ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")

    # 2. Create the ARP packet
    # pdst is the target IP range we want to query (e.g., 192.168.1.0/24)
    arp_packet = ARP(pdst=target_ip_range)

    # 3. Combine the two (Ether + ARP)
    packet = ether_frame / arp_packet

    # 4. Send and receive the packets
    # timeout=1: Wait max 1 second for a response
    # verbose=0: Don't show Scapy's internal output
    # 
    # REPLACE "Your Interface Name" with the actual name from Step 1
    interface_name = "Qualcomm QCA9377 802.11ac Wireless Adapter" 
    answered_list = srp(packet, timeout=1, verbose=0, iface=interface_name)[0]

    devices = []
    for sent, received in answered_list:
        devices.append({
            'ip': received.psrc,  # Source IP of the device that replied
            'mac': received.hwsrc # MAC address of the device that replied
        })
    
    return devices

# --- Main execution block ---
if __name__ == "__main__":
    # Example Target Range (REPLACE WITH YOUR LOCAL SUBNET!)
    # Use CIDR notation (e.g., '192.168.1.0/24')
    target_range = "192.168.1.0/24" 

    # Check if run as root/admin (Scapy needs privileged access)
    if not sys.platform.startswith('win') and sys.stdin.isatty():
        try:
            if sys.stdin.fileno() != 0:
                print("[-] You might need to run this with 'sudo' or as an administrator.")
        except AttributeError:
             pass # Windows doesn't usually hit this.

    active_devices = arp_scan(target_range)

    print("\n--- Found Devices ---")
    print("{:<15} {:<17}".format("IP Address", "MAC Address"))
    print("-" * 32)
    for device in active_devices:
        print("{:<15} {:<17}".format(device['ip'], device['mac']))