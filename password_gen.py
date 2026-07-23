#!/usr/bin/env python3
"""
PASSWORD GEN - Password Generator
Secure passwords, UUIDs, tokens and more.
"""

import os
import sys
import random
import string
import hashlib
import uuid
import secrets
import json
from datetime import datetime

def generate_password(length=16, use_upper=True, use_lower=True, use_digits=True, use_special=True):
    chars = ""
    required = []
    
    if use_lower:
        chars += string.ascii_lowercase
        required.append(random.choice(string.ascii_lowercase))
    if use_upper:
        chars += string.ascii_uppercase
        required.append(random.choice(string.ascii_uppercase))
    if use_digits:
        chars += string.digits
        required.append(random.choice(string.digits))
    if use_special:
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        chars += special
        required.append(random.choice(special))
    
    if not chars:
        chars = string.ascii_letters + string.digits
    
    remaining = [secrets.choice(chars) for _ in range(length - len(required))]
    password = required + remaining
    random.shuffle(password)
    
    return "".join(password)

def generate_passphrase(word_count=4):
    words = [
        "apple", "banana", "cherry", "dog", "elephant", "fox", "grape", "house",
        "igloo", "jungle", "kite", "lemon", "mountain", "night", "ocean", "piano",
        "queen", "river", "snake", "tiger", "umbrella", "village", "whale", "xylophone",
        "yellow", "zebra", "bridge", "castle", "dragon", "eagle", "forest", "garden",
        "harbor", "island", "jewel", "knight", "lantern", "mirror", "nebula", "oracle",
        "phoenix", "quartz", "robot", "shadow", "thunder", "utopia", "vortex", "winter",
        "crystal", "diamond", "ember", "falcon", "glacier", "horizon", "ivory", "jasper",
        "keystone", "lava", "marble", "nectar", "obsidian", "prism", "ruby", "sapphire",
        "topaz", "uranium", "velvet", "walrus", "xenon", "yacht", "zinc", "aurora",
        "blaze", "cipher", "delta", "echo", "frost", "glyph", "helix", "index"
    ]
    
    selected = [secrets.choice(words) for _ in range(word_count)]
    selected.append(str(secrets.randbelow(100)))
    return "-".join(selected)

def generate_pin(length=6):
    return "".join([str(secrets.randbelow(10)) for _ in range(length)])

def generate_uuid(version=4):
    if version == 4:
        return str(uuid.uuid4())
    elif version == 1:
        return str(uuid.uuid1())
    else:
        return str(uuid.uuid4())

def generate_token(length=32):
    return secrets.token_hex(length)

def generate_api_key():
    prefix = "sk-"
    token = secrets.token_hex(24)
    return prefix + token

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

def main():
    print("""
+========================================+
|        PASSWORD & SECURITY TOOL        |
+========================================+

  1. Generate password
  2. Generate passphrase
  3. Generate PIN
  4. Generate UUID
  5. Generate token
  6. Generate API key
  7. Hash text
  8. Batch generate
    """)
    
    choice = input(">> Choice [1-8]: ").strip()
    
    if choice == "1":
        length = input("Password length (Enter=16): ").strip()
        length = int(length) if length.isdigit() else 16
        
        use_upper = input("Uppercase? (Y/n): ").strip().lower() != "n"
        use_lower = input("Lowercase? (Y/n): ").strip().lower() != "n"
        use_digits = input("Digits? (Y/n): ").strip().lower() != "n"
        use_special = input("Special chars? (Y/n): ").strip().lower() != "n"
        
        print(f"\n  Password: {generate_password(length, use_upper, use_lower, use_digits, use_special)}")
    
    elif choice == "2":
        words = input("Number of words (Enter=4): ").strip()
        words = int(words) if words.isdigit() else 4
        print(f"\n  Passphrase: {generate_passphrase(words)}")
    
    elif choice == "3":
        length = input("PIN length (Enter=6): ").strip()
        length = int(length) if length.isdigit() else 6
        print(f"\n  PIN: {generate_pin(length)}")
    
    elif choice == "4":
        ver = input("UUID version (1/4, Enter=4): ").strip()
        version = int(ver) if ver in ("1", "4") else 4
        print(f"\n  UUID: {generate_uuid(version)}")
    
    elif choice == "5":
        length = input("Token length in chars (Enter=32): ").strip()
        length = int(length) if length.isdigit() else 32
        print(f"\n  Token: {generate_token(length)}")
    
    elif choice == "6":
        print(f"\n  API Key: {generate_api_key()}")
    
    elif choice == "7":
        text = input("Text to hash: ").strip()
        algo = input("Algorithm (md5/sha1/sha256/sha512, Enter=sha256): ").strip() or "sha256"
        result = hash_text(text, algo)
        if result:
            print(f"\n  {algo.upper()}: {result}")
        else:
            print("Unknown algorithm!")
    
    elif choice == "8":
        count = input("Number of passwords (Enter=10): ").strip()
        count = int(count) if count.isdigit() else 10
        length = input("Password length (Enter=16): ").strip()
        length = int(length) if length.isdigit() else 16
        
        print(f"\n  Generated passwords:\n")
        for i in range(count):
            print(f"  {i+1:3}. {generate_password(length)}")
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
