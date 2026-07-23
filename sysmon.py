#!/usr/bin/env python3
"""
SYSMON - System Monitor
Real-time monitoring of CPU, RAM, disk and processes.
"""

import os
import sys
import time
import psutil
from datetime import datetime

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def human_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}PB"

def get_bar(percent, length=30):
    filled = int(length * percent / 100)
    return "[" + "#" * filled + "-" * (length - filled) + "]"

def show_cpu():
    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    
    print(f"\n  CPU:")
    print(f"    Load:       {get_bar(cpu_percent)} {cpu_percent:.1f}%")
    print(f"    Cores:      {cpu_count}")
    if cpu_freq:
        print(f"    Frequency:  {cpu_freq.current:.0f} MHz / {cpu_freq.max:.0f} MHz")
    
    per_core = psutil.cpu_percent(interval=0.1, percpu=True)
    if len(per_core) <= 16:
        print(f"    Per-core:")
        for i, pct in enumerate(per_core):
            print(f"      Core {i:2}: {get_bar(pct, 20)} {pct:.1f}%")

def show_memory():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    print(f"\n  RAM:")
    print(f"    Total:      {human_size(mem.total)}")
    print(f"    Used:       {human_size(mem.used)} ({mem.percent}%)")
    print(f"    Free:       {human_size(mem.available)}")
    print(f"    Load:       {get_bar(mem.percent)}")
    
    print(f"\n  SWAP:")
    print(f"    Total:      {human_size(swap.total)}")
    print(f"    Used:       {human_size(swap.used)} ({swap.percent}%)")
    print(f"    Load:       {get_bar(swap.percent)}")

def show_disk():
    print(f"\n  DISKS:")
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            print(f"    {part.device:6} {part.mountpoint:4} {get_bar(usage.percent)} {usage.percent}%")
            print(f"             {human_size(usage.used)} / {human_size(usage.total)}")
        except:
            pass

def show_network():
    net = psutil.net_io_counters()
    
    print(f"\n  NETWORK:")
    print(f"    Sent:       {human_size(net.bytes_sent)}")
    print(f"    Received:   {human_size(net.bytes_recv)}")
    print(f"    Packets:    {net.packets_sent:,} / {net.packets_recv:,}")

def show_top_processes(n=10):
    procs = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            procs.append(proc.info)
        except:
            pass
    
    procs.sort(key=lambda x: x['memory_percent'] or 0, reverse=True)
    
    print(f"\n  TOP PROCESSES (by RAM):")
    print(f"    {'PID':>6}  {'CPU%':>5}  {'RAM%':>6}  Name")
    print(f"    {'-'*50}")
    for p in procs[:n]:
        print(f"    {p['pid']:>6}  {p['cpu_percent'] or 0:>5.1f}  {p['memory_percent'] or 0:>6.1f}  {p['name']}")

def show_battery():
    bat = psutil.sensors_battery()
    if bat:
        print(f"\n  BATTERY:")
        print(f"    Status:     {get_bar(bat.percent)} {bat.percent}%")
        print(f"    Charging:   {'Yes' if bat.power_plugged else 'No'}")
        if bat.secsleft and bat.secsleft > 0:
            hours = bat.secsleft // 3600
            mins = (bat.secsleft % 3600) // 60
            print(f"    Remaining:  {hours}h {mins}m")

def monitor_loop():
    print("SYSMON - Press Ctrl+C to quit\n")
    
    try:
        while True:
            clear()
            
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{'='*60}")
            print(f"  SYSMON - System Monitor | {now}")
            print(f"{'='*60}")
            
            show_cpu()
            show_memory()
            show_disk()
            show_network()
            show_battery()
            
            print(f"\n{'='*60}")
            print(f"  Ctrl+C to quit | Refresh: 2s")
            
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n\nExited.")

def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd == "cpu":
            show_cpu()
        elif cmd == "ram" or cmd == "memory":
            show_memory()
        elif cmd == "disk":
            show_disk()
        elif cmd == "net" or cmd == "network":
            show_network()
        elif cmd == "proc" or cmd == "processes":
            show_top_processes(20)
        elif cmd == "bat" or cmd == "battery":
            show_battery()
        elif cmd == "all":
            show_cpu()
            show_memory()
            show_disk()
            show_network()
            show_battery()
        else:
            print("Usage: sysmon [cpu|ram|disk|net|proc|bat|all]")
            print("No args = continuous monitoring")
    else:
        monitor_loop()

if __name__ == "__main__":
    main()
