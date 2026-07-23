#!/usr/bin/env python3
"""
JSON TOOL - JSON Operations
Format, validate, convert, search.
"""

import os
import sys
import json
from pathlib import Path

def format_json(filepath, indent=2):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    formatted = json.dumps(data, indent=indent, ensure_ascii=False)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(formatted)
    print(f"  Formatted: {filepath}")
    return True

def validate_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"  Valid JSON: {filepath}")
    print(f"  Type: {type(data).__name__}")
    if isinstance(data, dict):
        print(f"  Keys: {len(data)}")
    elif isinstance(data, list):
        print(f"  Items: {len(data)}")
    return True

def minify_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    minified = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(minified)
    print(f"  Minified: {filepath}")

def search_json(filepath, query):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    results = []
    search_recursive(data, query.lower(), [], results)
    if results:
        for path, value in results:
            print(f"  {path} = {value}")
    else:
        print("  Nothing found.")

def search_recursive(obj, query, path, results):
    if isinstance(obj, dict):
        for key, val in obj.items():
            new_path = f"{path}.{key}" if path else key
            if query in str(key).lower():
                results.append((new_path, val))
            search_recursive(val, query, new_path, results)
    elif isinstance(obj, list):
        for i, val in enumerate(obj):
            new_path = f"{path}[{i}]"
            search_recursive(val, query, new_path, results)

def json_to_csv(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        print("  JSON must be an array of records!")
        return
    if not data:
        print("  Empty array!")
        return
    headers = list(data[0].keys())
    out_path = filepath.rsplit(".", 1)[0] + ".csv"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(",".join(headers) + "\n")
        for row in data:
            vals = [str(row.get(h, "")).replace(",", ";") for h in headers]
            f.write(",".join(vals) + "\n")
    print(f"  Exported: {out_path}")

def json_to_yaml_lite(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    out_path = filepath.rsplit(".", 1)[0] + ".yaml"
    with open(out_path, "w", encoding="utf-8") as f:
        yaml_dump(data, f, 0)
    print(f"  Exported: {out_path}")

def yaml_dump(data, f, indent):
    prefix = "  " * indent
    if isinstance(data, dict):
        for key, val in data.items():
            if isinstance(val, (dict, list)):
                f.write(f"{prefix}{key}:\n")
                yaml_dump(val, f, indent + 1)
            else:
                f.write(f"{prefix}{key}: {val}\n")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                f.write(f"{prefix}-\n")
                yaml_dump(item, f, indent + 1)
            else:
                f.write(f"{prefix}- {item}\n")

def inspect_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    size = os.path.getsize(filepath)
    print(f"  File: {filepath}")
    print(f"  Size: {size} B ({size/1024:.1f} KB)")
    print(f"  Type: {type(data).__name__}")
    depth = get_depth(data)
    print(f"  Depth: {depth}")
    keys = count_keys(data)
    print(f"  Total keys: {keys}")

def get_depth(obj, current=0):
    if isinstance(obj, dict):
        if not obj:
            return current
        return max(get_depth(v, current + 1) for v in obj.values())
    elif isinstance(obj, list):
        if not obj:
            return current
        return max(get_depth(v, current + 1) for v in obj)
    return current

def count_keys(obj):
    if isinstance(obj, dict):
        return len(obj) + sum(count_keys(v) for v in obj.values())
    elif isinstance(obj, list):
        return sum(count_keys(v) for v in obj)
    return 0

def main():
    print("""
+========================================+
|           JSON TOOL                    |
+========================================+

  1. Format JSON
  2. Validate JSON
  3. Minify JSON
  4. Search in JSON
  5. JSON -> CSV
  6. JSON -> YAML
  7. Inspect JSON
    """)
    choice = input(">> Choice [1-7]: ").strip()
    filepath = input("Path to JSON file: ").strip()
    if not os.path.exists(filepath):
        print("File not found!")
        return
    try:
        if choice == "1":
            indent = input("Indent (Enter=2): ").strip()
            indent = int(indent) if indent.isdigit() else 2
            format_json(filepath, indent)
        elif choice == "2":
            validate_json(filepath)
        elif choice == "3":
            minify_json(filepath)
        elif choice == "4":
            query = input("Search: ").strip()
            search_json(filepath, query)
        elif choice == "5":
            json_to_csv(filepath)
        elif choice == "6":
            json_to_yaml_lite(filepath)
        elif choice == "7":
            inspect_json(filepath)
        else:
            print("Invalid choice!")
    except Exception as e:
        print(f"  Error: {e}")

if __name__ == "__main__":
    main()
