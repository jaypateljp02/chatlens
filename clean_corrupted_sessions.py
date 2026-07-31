import os
import json

STORAGE_DIR = os.path.join(os.path.dirname(__file__), "backend", "uploads", "sessions")
cleaned = 0

if os.path.exists(STORAGE_DIR):
    for fname in os.listdir(STORAGE_DIR):
        if fname.endswith(".json"):
            fpath = os.path.join(STORAGE_DIR, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    json.load(f)
            except Exception as e:
                print(f"[CLEANED] Removing corrupted session file {fname}: {e}")
                os.remove(fpath)
                cleaned += 1

print(f"Cleaned {cleaned} corrupted session files.")
