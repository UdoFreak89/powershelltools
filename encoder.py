#!/usr/bin/env python3
"""
ENCODE - Encoder/Decoder
Base64, URL, Hex, HTML, ROT13 and more.
"""

import os
import sys
import base64
import urllib.parse
import binascii
import html
import codecs

def base64_encode(text):
    return base64.b64encode(text.encode()).decode()

def base64_decode(text):
    return base64.b64decode(text).decode()

def url_encode(text):
    return urllib.parse.quote(text)

def url_decode(text):
    return urllib.parse.unquote(text)

def url_encode_plus(text):
    return urllib.parse.quote_plus(text)

def url_decode_plus(text):
    return urllib.parse.unquote_plus(text)

def hex_encode(text):
    return binascii.hexlify(text.encode()).decode()

def hex_decode(text):
    return binascii.unhexlify(text).decode()

def html_encode(text):
    return html.escape(text)

def html_decode(text):
    return html.unescape(text)

def rot13(text):
    return codecs.decode(text, 'rot_13')

def binary_encode(text):
    return " ".join(format(ord(c), '08b') for c in text)

def binary_decode(text):
    return "".join(chr(int(b, 2)) for b in text.split() if b)

def morse_encode(text):
    morse = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....',
        '7': '--...', '8': '---..', '9': '----.', ' ': '/'
    }
    return " ".join(morse.get(c.upper(), '') for c in text)

def morse_decode(text):
    morse = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
        '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
        '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
        '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
        '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
        '--..': 'Z', '-----': '0', '.----': '1', '..---': '2',
        '...--': '3', '....-': '4', '.....': '5', '-....': '6',
        '--...': '7', '---..': '8', '----.': '9', '/': ' '
    }
    return "".join(morse.get(c, '') for c in text.split())

def main():
    print("""
+========================================+
|           ENCODE / DECODE              |
+========================================+

  1. Base64 Encode
  2. Base64 Decode
  3. URL Encode
  4. URL Decode
  5. Hex Encode
  6. Hex Decode
  7. HTML Encode
  8. HTML Decode
  9. ROT13
  10. Binary Encode
  11. Binary Decode
  12. Morse Encode
  13. Morse Decode
    """)
    
    choice = input(">> Choice [1-13]: ").strip()
    text = input("\nText: ").strip()
    
    if not text:
        print("No text provided!")
        return
    
    results = {
        "1": ("Base64", base64_encode),
        "2": ("Base64", base64_decode),
        "3": ("URL", url_encode),
        "4": ("URL", url_decode),
        "5": ("Hex", hex_encode),
        "6": ("Hex", hex_decode),
        "7": ("HTML", html_encode),
        "8": ("HTML", html_decode),
        "9": ("ROT13", rot13),
        "10": ("Binary", binary_encode),
        "11": ("Binary", binary_decode),
        "12": ("Morse", morse_encode),
        "13": ("Morse", morse_decode),
    }
    
    if choice in results:
        name, func = results[choice]
        try:
            result = func(text)
            print(f"\n  {name}: {result}")
        except Exception as e:
            print(f"\n  Error: {e}")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
