#!/usr/bin/env python3
"""
GIT HELPER - Git Shortcuts & Assistant
Status, commit, push, pull, log, diff and more.
"""

import os
import sys
import subprocess
from datetime import datetime

def run(cmd, cwd=None):
    result = subprocess.run(
        cmd, capture_output=True, text=True, shell=True, cwd=cwd
    )
    return result.stdout.strip(), result.returncode

def is_git_repo(path):
    out, code = run("git rev-parse --is-inside-work-tree", cwd=path)
    return code == 0 and out == "true"

def git_status(path):
    out, _ = run("git status --short", cwd=path)
    if not out:
        print("  Working tree clean.")
    else:
        print(f"\n  Changes:\n")
        for line in out.split("\n"):
            print(f"    {line}")

def git_log(path, count=10):
    out, _ = run(f'git log --oneline -{count}', cwd=path)
    if out:
        print(f"\n  Last {count} commits:\n")
        for line in out.split("\n"):
            print(f"    {line}")
    else:
        print("  No commits.")

def git_diff(path, staged=False):
    flag = "--cached" if staged else ""
    out, _ = run(f"git diff {flag}", cwd=path)
    if out:
        print(f"\n  Diff:\n")
        print(out)
    else:
        print("  No changes.")

def git_add_all(path):
    out, code = run("git add -A", cwd=path)
    if code == 0:
        print("  All files staged.")
    else:
        print(f"  Error: {out}")

def git_commit(path, message):
    out, code = run(f'git commit -m "{message}"', cwd=path)
    if code == 0:
        print(f"  Commit created: {message}")
    else:
        print(f"  Error: {out}")

def git_push(path, remote="origin"):
    out, code = run(f"git push {remote}", cwd=path)
    if code == 0:
        print(f"  Pushed to {remote}.")
    else:
        print(f"  Error: {out}")

def git_pull(path, remote="origin"):
    out, code = run(f"git pull {remote}", cwd=path)
    if code == 0:
        print(f"  Pulled from {remote}.")
    else:
        print(f"  Error: {out}")

def git_branches(path):
    out, _ = run("git branch -a", cwd=path)
    if out:
        print(f"\n  Branches:\n")
        for line in out.split("\n"):
            print(f"    {line}")

def git_clone(url, target=None):
    cmd = f"git clone {url}"
    if target:
        cmd += f" {target}"
    out, code = run(cmd)
    if code == 0:
        print(f"  Cloned: {url}")
    else:
        print(f"  Error: {out}")

def git_stash(path):
    out, code = run("git stash", cwd=path)
    if code == 0:
        print(f"  Stashed: {out}")
    else:
        print(f"  Error: {out}")

def git_stash_pop(path):
    out, code = run("git stash pop", cwd=path)
    if code == 0:
        print(f"  Stash restored.")
    else:
        print(f"  Error: {out}")

def git_blame(path, filepath):
    out, _ = run(f"git blame {filepath}", cwd=path)
    if out:
        print(f"\n  Blame for {filepath}:\n")
        print(out)
    else:
        print("  File not found in git.")

def git_ignore_add(path, pattern):
    gitignore = os.path.join(path, ".gitignore")
    with open(gitignore, "a", encoding="utf-8") as f:
        f.write(pattern + "\n")
    print(f"  Added to .gitignore: {pattern}")

def git_quick_commit(path, message):
    git_add_all(path)
    git_commit(path, message)

def main():
    print("""
+========================================+
|           GIT HELPER                   |
+========================================+

  1. Status
  2. Log
  3. Diff
  4. Diff (staged)
  5. Add all + Commit
  6. Push
  7. Pull
  8. Branches
  9. Clone
  10. Stash
  11. Stash Pop
  12. Blame
  13. Add to .gitignore
    """)
    choice = input(">> Choice [1-13]: ").strip()
    path = input("Repo path (Enter=.): ").strip() or "."

    if not is_git_repo(path):
        print("  Not a git repo!")
        return

    if choice == "1":
        git_status(path)
    elif choice == "2":
        n = input("Count (Enter=10): ").strip()
        n = int(n) if n.isdigit() else 10
        git_log(path, n)
    elif choice == "3":
        git_diff(path, staged=False)
    elif choice == "4":
        git_diff(path, staged=True)
    elif choice == "5":
        msg = input("Commit message: ").strip()
        if msg:
            git_quick_commit(path, msg)
        else:
            print("Enter a message!")
    elif choice == "6":
        git_push(path)
    elif choice == "7":
        git_pull(path)
    elif choice == "8":
        git_branches(path)
    elif choice == "9":
        url = input("Repo URL: ").strip()
        target = input("Target folder (Enter=auto): ").strip() or None
        git_clone(url, target)
    elif choice == "10":
        git_stash(path)
    elif choice == "11":
        git_stash_pop(path)
    elif choice == "12":
        fp = input("File path: ").strip()
        git_blame(path, fp)
    elif choice == "13":
        pat = input("Pattern: ").strip()
        git_ignore_add(path, pat)
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
