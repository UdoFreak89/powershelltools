#!/usr/bin/env python3
"""
NETWORK TOOL - Network utilities
Ping, traceroute, DNS, port scan, IP info.
"""

import os
import sys
import socket
import subprocess
import struct
import time
import concurrent.futures

def ping_host(host, count=4):
    print(f"\n  PING {host}:\n")
    result = subprocess.run(
        ["ping", "-n", str(count), host],
        capture_output=True, text=True, timeout=30
    )
    print(result.stdout)
    if result.returncode != 0 and result.stderr:
        print(result.stderr)

def dns_lookup(host):
    print(f"\n  DNS for {host}:\n")
    try:
        results = socket.getaddrinfo(host, None)
        seen = set()
        for res in results:
            family, _, _, _, addr = res
            ip = addr[0]
            fam_name = "IPv4" if family == socket.AF_INET else "IPv6"
            key = (fam_name, ip)
            if key not in seen:
                seen.add(key)
                print(f"    {fam_name}: {ip}")
    except socket.gaierror as e:
        print(f"    Error: {e}")

def reverse_dns(ip):
    print(f"\n  Reverse DNS for {ip}:\n")
    try:
        hostname = socket.gethostbyaddr(ip)
        print(f"    Hostname: {hostname[0]}")
        if hostname[1]:
            print(f"    Aliases: {', '.join(hostname[1])}")
    except socket.herror:
        print("    Not found.")

def port_scan(host, start_port=1, end_port=1024, timeout=0.5):
    print(f"\n  Port scan {host} ({start_port}-{end_port}):\n")
    open_ports = []

    def check_port(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            s.close()
            return port if result == 0 else None
        except:
            return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(check_port, p): p for p in range(start_port, end_port + 1)}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)
                try:
                    service = socket.getservbyport(result)
                except:
                    service = "?"
                print(f"    Port {result:5d} OPEN  ({service})")

    print(f"\n  Total open: {len(open_ports)}")

def port_check(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        result = s.connect_ex((host, int(port)))
        s.close()
        if result == 0:
            print(f"  Port {port} on {host}: OPEN")
        else:
            print(f"  Port {port} on {host}: CLOSED")
    except Exception as e:
        print(f"  Error: {e}")

def traceroute(host, max_hops=30):
    print(f"\n  TRACEROUTE {host}:\n")
    result = subprocess.run(
        ["tracert", "-d", "-h", str(max_hops), host],
        capture_output=True, text=True, timeout=60
    )
    print(result.stdout)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def host_info(host):
    print(f"\n  Info about {host}:\n")
    try:
        ip = socket.gethostbyname(host)
        print(f"    IP: {ip}")
        parts = ip.split(".")
        if parts[0] == "10" or parts[0] == "127":
            print(f"    Type: Private network")
        elif parts[0] == "192" and parts[1] == "168":
            print(f"    Type: Private network")
        elif parts[0] == "172" and 16 <= int(parts[1]) <= 31:
            print(f"    Type: Private network")
        else:
            print(f"    Type: Public IP")
    except socket.gaierror:
        print(f"    Cannot resolve.")

def main():
    print("""
+========================================+
|         NETWORK TOOL                   |
+========================================+

  1. Ping
  2. DNS Lookup
  3. Reverse DNS
  4. Port Scan
  5. Port Check
  6. Traceroute
  7. My IP
  8. Host Info
    """)
    choice = input(">> Choice [1-8]: ").strip()
    if choice == "1":
        host = input("Host: ").strip()
        count = input("Count (Enter=4): ").strip()
        count = int(count) if count.isdigit() else 4
        ping_host(host, count)
    elif choice == "2":
        host = input("Host: ").strip()
        dns_lookup(host)
    elif choice == "3":
        ip = input("IP address: ").strip()
        reverse_dns(ip)
    elif choice == "4":
        host = input("Host: ").strip()
        start = input("Start port (Enter=1): ").strip()
        end = input("End port (Enter=1024): ").strip()
        start = int(start) if start.isdigit() else 1
        end = int(end) if end.isdigit() else 1024
        port_scan(host, start, end)
    elif choice == "5":
        host = input("Host: ").strip()
        port = input("Port: ").strip()
        port_check(host, port)
    elif choice == "6":
        host = input("Host: ").strip()
        traceroute(host)
    elif choice == "7":
        ip = get_local_ip()
        print(f"\n  Local IP: {ip}")
    elif choice == "8":
        host = input("Host: ").strip()
        host_info(host)
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
