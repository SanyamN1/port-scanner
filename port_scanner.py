from scapy.all import IP, TCP, sr1, RandShort
import random
import threading
import time

# Target configuration
target_ip = "192.168.1.1"
port_range = range(1, 1025)  # You can expand this up to 65535
thread_count = 100

open_ports = []

def stealth_scan(port):
    # Craft IP and TCP SYN packet
    ip = IP(dst=target_ip)
    tcp = TCP(sport=RandShort(), dport=port, flags="S")
    
    # Send SYN, wait for SYN-ACK (timeout = 1s)
    response = sr1(ip/tcp, timeout=1, verbose=0)

    if response is not None:
        if response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12:
            print(f"[OPEN] Port {port}")
            open_ports.append(port)
            # Send RST to close (no handshake)
            rst = TCP(sport=RandShort(), dport=port, flags="R")
            sr1(ip/rst, timeout=0.5, verbose=0)
    
    # Randomized sleep to avoid detection
    time.sleep(random.uniform(0.01, 0.1))

def run_scan():
    ports = list(port_range)
    random.shuffle(ports)  # Random scan order
    
    threads = []
    for port in ports:
        t = threading.Thread(target=stealth_scan, args=(port,))
        threads.append(t)
        t.start()

        while threading.active_count() > thread_count:
            time.sleep(0.05)

    for t in threads:
        t.join()

    print("\nScan complete.")
    print("Open Ports:", open_ports)

if __name__ == "__main__":
    run_scan()

