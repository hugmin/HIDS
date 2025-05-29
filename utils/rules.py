import json

def load_malicious_hashes(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return set(json.load(f))  # List -> Set for fast lookup
    except Exception:
        return set()
