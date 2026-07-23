#!/usr/bin/env python3
"""
TIMER - Timer and Stopwatch
Countdowns, stopwatch, Pomodoro, alarm.
"""

import os
import sys
import time
from datetime import datetime, timedelta

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def countdown_timer(hours=0, minutes=0, seconds=0):
    total = hours * 3600 + minutes * 60 + seconds
    
    if total <= 0:
        print("Time must be greater than 0!")
        return
    
    print(f"TIMER: {format_time(total)}")
    print("Press Ctrl+C to stop\n")
    
    try:
        while total > 0:
            clear()
            print(f"""
+========================================+
|              TIMER                     |
+========================================+

            {format_time(total)}

            Time remaining...
            
+========================================+
|  Ctrl+C to stop                        |
+========================================+
            """)
            time.sleep(1)
            total -= 1
        
        print("\a" * 5)
        print("\nTIME'S UP!")
        
    except KeyboardInterrupt:
        print(f"\nStopped. Remaining: {format_time(total)}")

def stopwatch():
    print("STOPWATCH")
    print("Press Enter to START")
    input()
    
    start = time.time()
    print("Running... Press Enter to STOP")
    
    try:
        while True:
            elapsed = time.time() - start
            clear()
            print(f"""
+========================================+
|             STOPWATCH                  |
+========================================+

            {format_time(elapsed)}

            Running...
            
+========================================+
|  Enter to STOP                         |
+========================================+
            """)
            
            if os.name == "nt":
                import msvcrt
                if msvcrt.kbhit():
                    if msvcrt.getch() == b'\r':
                        break
            else:
                import select
                if select.select([sys.stdin], [], [], 0)[0]:
                    sys.stdin.readline()
                    break
            
            time.sleep(0.1)
        
        elapsed = time.time() - start
        print(f"\nStopped: {format_time(elapsed)}")
        
    except KeyboardInterrupt:
        elapsed = time.time() - start
        print(f"\nStopped: {format_time(elapsed)}")

def pomodoro(work_min=25, break_min=5):
    print(f"POMODORO: {work_min} min work, {break_min} min break")
    print("Press Enter to start\n")
    input()
    
    cycles = 0
    
    try:
        while True:
            cycles += 1
            print(f"\n=== CYCLE {cycles} ===")
            
            print(f"\nWORK ({work_min} min)...")
            countdown_timer(0, work_min, 0)
            
            print(f"\nBREAK ({break_min} min)...")
            countdown_timer(0, break_min, 0)
            
            print(f"\nCycle {cycles} complete!")
            input("Enter for next cycle (Ctrl+C to quit)")
    
    except KeyboardInterrupt:
        print(f"\nCompleted {cycles} cycles!")

def alarm(hour, minute):
    now = datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0)
    
    if target < now:
        target += timedelta(days=1)
    
    diff = (target - now).total_seconds()
    
    print(f"ALARM: Set for {hour:02d}:{minute:02d}")
    print(f"In: {format_time(diff)}")
    print("Press Ctrl+C to cancel\n")
    
    try:
        while True:
            now = datetime.now()
            if now.hour == hour and now.minute == minute:
                print("\a" * 10)
                print("\nALARM! ALARM! ALARM!")
                break
            
            remaining = (target - datetime.now()).total_seconds()
            if remaining <= 0:
                print("\a" * 10)
                print("\nALARM! ALARM! ALARM!")
                break
            
            clear()
            print(f"""
+========================================+
|               ALARM                    |
+========================================+

            {hour:02d}:{minute:02d}

            Remaining: {format_time(remaining)}
            
+========================================+
|  Ctrl+C to cancel                      |
+========================================+
            """)
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nAlarm cancelled.")

def main():
    print("""
+========================================+
|           TIMER & STOPWATCH            |
+========================================+

  1. Timer (countdown)
  2. Stopwatch
  3. Pomodoro
  4. Alarm
    """)
    
    choice = input(">> Choice [1-4]: ").strip()
    
    if choice == "1":
        h = input("Hours (Enter=0): ").strip()
        m = input("Minutes (Enter=5): ").strip()
        s = input("Seconds (Enter=0): ").strip()
        
        hours = int(h) if h.isdigit() else 0
        minutes = int(m) if m.isdigit() else 5
        seconds = int(s) if s.isdigit() else 0
        
        countdown_timer(hours, minutes, seconds)
    
    elif choice == "2":
        stopwatch()
    
    elif choice == "3":
        work = input("Work minutes (Enter=25): ").strip()
        brk = input("Break minutes (Enter=5): ").strip()
        
        work_min = int(work) if work.isdigit() else 25
        break_min = int(brk) if brk.isdigit() else 5
        
        pomodoro(work_min, break_min)
    
    elif choice == "4":
        h = input("Hour (0-23): ").strip()
        m = input("Minute (0-59): ").strip()
        
        if h.isdigit() and m.isdigit():
            alarm(int(h), int(m))
        else:
            print("Invalid time!")
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
