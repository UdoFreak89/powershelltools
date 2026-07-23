#!/usr/bin/env python3
"""
HASH TOOL - Hash Generator
MD5, SHA1, SHA256, SHA512 and more.
"""

import os
import sys
import hashlib
import base64
import binascii
import json
from pathlib import Path

def hash_file(filepath, algorithm="sha256"):
    algorithms = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
    }
    
    if algorithm not in algorithms:
        return None
    
    h = algorithms[algorithm]()
    
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    
    return h.hexdigest()

def hash_text(text, algorithm="sha256"):
    algorithms = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
    }
    
    if algorithm not in algorithms:
        return None
    
    h = algorithms[algorithm]()
    h.update(text.encode("utf-8"))
    return h.hexdigest()

def hash_all(filepath):
    results = {}
    for algo in ["md5", "sha1", "sha256", "sha512"]:
        results[algo] = hash_file(filepath, algo)
    return results

def compare_hashes(file1, file2):
    print(f"\nComparison:\n  {file1}\n  {file2}\n")
    
    for algo in ["md5", "sha1", "sha256"]:
        hash1 = hash_file(file1, algo)
        hash2 = hash_file(file2, algo)
        
        if hash1 and hash2:
            match = "MATCH" if hash1 == hash2 else "DIFFER"
            print(f"  {algo.upper():8} [{match}]")
            print(f"    {hash1}")
            print(f"    {hash2}")

def main():
    print("""
+========================================+
|           HASH TOOL                    |
+========================================+

  1. Hash a file
  2. Hash text
  3. All hashes for a file
  4. Compare two files
  5. Search in file (hex)
    """)
    
    choice = input(">> Choice [1-5]: ").strip()
    
    if choice == "1":
        filepath = input("File path: ").strip()
        algo = input("Algorithm (md5/sha1/sha256/sha512, Enter=sha256): ").strip() or "sha256"
        
        if os.path.exists(filepath):
            result = hash_file(filepath, algo)
            print(f"\n  {algo.upper()}: {result}")
        else:
            print("File not found!")
    
    elif choice == "2":
        text = input("Text: ").strip()
        algo = input("Algorithm (Enter=sha256): ").strip() or "sha256"
        
        result = hash_text(text, algo)
        if result:
            print(f"\n  {algo.upper()}: {result}")
        else:
            print("Unknown algorithm!")
    
    elif choice == "3":
        filepath = input("File path: ").strip()
        
        if os.path.exists(filepath):
            results = hash_all(filepath)
            print(f"\n  Hashes for {filepath}:\n")
            for algo, hash_val in results.items():
                print(f"  {algo.upper():8} {hash_val}")
        else:
            print("File not found!")
    
    elif choice == "4":
        file1 = input("File 1: ").strip()
        file2 = input("File 2: ").strip()
        
        if os.path.exists(file1) and os.path.exists(file2):
            compare_hashes(file1, file2)
        else:
            print("One or both files not found!")
    
    elif choice == "5":
        filepath = input("File path: ").strip()
        hex_str = input("Hex string to search: ").strip()
        
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                content = f.read()
            
            try:
                search_bytes = binascii.unhexlify(hex_str)
                pos = content.find(search_bytes)
                
                if pos >= 0:
                    print(f"\n  Found at position {pos} (0x{pos:X})")
                    start = max(0, pos - 16)
                    end = min(len(content), pos + len(search_bytes) + 16)
                    context = content[start:end]
                    print(f"  Context: {binascii.hexlify(context).decode()}")
                else:
                    print("\n  Not found!")
            except:
                print("Invalid hex format!")
        else:
            print("File not found!")
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
