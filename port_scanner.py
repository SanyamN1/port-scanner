import os
import random
import threading
import time
import socket
from scapy.all import IP, TCP, sr1, RandShort

# Colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Snake-with-Goggles Banner
BANNER = f"""
{GREEN}        /^\\/^\\
      _|__|  O|
\\/     /~     \\_/ \\
 \\____|__________/  \\
        \\_______      \\
                `\\     \\                 \\
                  |     |                  \\
                 /      /                    \\
                /     /                       \\\\
              /      /                         \\ \\
             /     /                            \\  \\
           /     /             _----_            \\   \\
          /     /           _-~      ~-_         |   |
         (      (        _-~          ~-_     _/
          \\      ~-____-~    {YELLOW}O O{GREEN}     ~-_   _/
            ~-_           _-~           _-~    /
               ~--______-~          _-~
                              _ - ~
{RESET}
"""

open_ports = []
target_ip = ""
port_range = range(1, 1025)
thread_count = 100
delay_range = (0.01, 0.1)

# Clear screen
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# Banner grabbing
def service_detection(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((ip, port))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = s.recv(1024).decode(errors="ignore").strip()
        s.close()
        return banner if banner else "Unknown"
    except:
        return "No banner"

# Basic OS detection using TTL heuristic
def os_detection(ip):
    pkt = IP(dst=ip)/TCP(dport=80, flags="S")
    resp = sr1(pkt, timeout=1, verbose=0)
    if resp:
        ttl = resp.ttl
        if ttl >= 128:
            return "Windows (probable)"
        elif ttl >= 64:
            return "Linux/Unix (probable)"
    return "Unknown"

# SYN Scan
def stealth_scan(port, do_service=False):
    global target_ip
    ip = IP(dst=target_ip)
    tcp = TCP(sport=RandShort(), dport=port, flags="S")
    response = sr1(ip/tcp, timeout=1, verbose=0)

    if response and response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12:
        if do_service:
            banner = service_detection(target_ip, port)
            print(f"{GREEN}[OPEN]{RESET} Port {port} → {CYAN}{banner}{RESET}")
        else:
            print(f"{GREEN}[OPEN]{RESET} Port {port}")
        open_ports.append(port)
        rst = TCP(sport=RandShort(), dport=port, flags="R")
        sr1(ip/rst, timeout=0.5, verbose=0)

    time.sleep(random.uniform(*delay_range))

def run_scan(do_service=False):
    ports = list(port_range)
    random.shuffle(ports)
    threads = []

    for port in ports:
        t = threading.Thread(target=stealth_scan, args=(port, do_service))
        threads.append(t)
        t.start()

        while threading.active_count() > thread_count:
            time.sleep(0.05)

    for t in threads:
        t.join()

    print("\nScan complete.")
    print("Open Ports:", open_ports)

def menu():
    global target_ip, port_range, thread_count, delay_range
    while True:
        clear()
        print(BANNER)
        print("[1] Extreme Stealth Scan")
        print("[2] Extreme Aggressive Scan")
        print("[3] Full Power Scan (1–65535)")
        print("[4] Custom Range Scan")
        print("[5] Full Recon Mode (Scan + Service + OS)")
        print("[6] Exit")

        choice = input("\nSelect mode: ").strip()
        if choice == "6":
            break

        target_ip = input("Enter Target IP: ").strip()
        open_ports.clear()

        if choice == "1":
            port_range = range(1, 1025)
            thread_count = 50
            delay_range = (0.2, 0.5)
            clear(); print(BANNER)
            run_scan()
        elif choice == "2":
            port_range = range(1, 1025)
            thread_count = 500
            delay_range = (0.001, 0.01)
            clear(); print(BANNER)
            run_scan()
        elif choice == "3":
            port_range = range(1, 65536)
            thread_count = 500
            delay_range = (0.001, 0.01)
            clear(); print(BANNER)
            run_scan()
        elif choice == "4":
            start = int(input("Start Port: "))
            end = int(input("End Port: "))
            port_range = range(start, end + 1)
            thread_count = int(input("Threads (e.g., 100): "))
            delay_min = float(input("Min Delay (sec): "))
            delay_max = float(input("Max Delay (sec): "))
            delay_range = (delay_min, delay_max)
            clear(); print(BANNER)
            run_scan()
        elif choice == "5":
            port_range = range(1, 1025)
            thread_count = 100
            delay_range = (0.05, 0.2)
            clear(); print(BANNER)
            run_scan(do_service=True)
            print(f"\n{YELLOW}OS Detection: {os_detection(target_ip)}{RESET}")
        else:
            input("Invalid choice. Press Enter...")

        input("\nPress Enter to return to menu...")

if __name__ == "__main__":
    menu()

