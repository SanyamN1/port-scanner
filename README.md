# port-scanner

# 🔍 Stealth SYN Port Scanner

A high-speed, stealthy, and aggressive TCP SYN port scanner written in Python using `scapy`. This tool allows you to scan a target host for open ports without completing TCP handshakes, reducing the chance of detection by firewalls, intrusion detection systems (IDS), and logging mechanisms.

---

## ⚠️ Legal Notice

> **This tool is intended strictly for educational purposes or authorized penetration testing.**
>
> Scanning or probing systems you do not own or have explicit permission to assess is **illegal** and may result in **criminal charges**. Always act responsibly and ethically. The author is **not liable** for any misuse of this software.

---

## 🛠️ Features

- 🔎 **SYN Scan (Half-open)** – Sends TCP SYN packets and listens for SYN-ACK without completing handshakes.
- 🧬 **Raw socket packet crafting** – Uses `scapy` for precise control over packets.
- 🎲 **Randomized scan order** – Ports are scanned in shuffled order to avoid detection patterns.
- 🕵️ **Low-profile threading with jitter** – Threads are capped and randomized sleep intervals reduce noise.
- 🚫 **No dependency on external tools** like Nmap or masscan.

---
🧪 How It Works
Sends SYN packets to each target port using randomized source ports.

Waits for SYN-ACK responses — indicates port is open.

Does not complete handshake (no ACK), making detection harder.

If SYN-ACK received, sends a RST to avoid leaving open connections.

---

## 📦 Requirements

- Python 3.x
- `scapy` library  
  Install with:
  ```bash
  pip install scapy

Run as root or with administrative privileges (raw socket access is required):
- sudo python3 stealth_syn_scanner.py

To scan different IPs or port ranges, edit these lines at the top of the script:
-target_ip = "192.168.1.1"
-port_range = range(1, 1025)  # You can extend this up to 65535
