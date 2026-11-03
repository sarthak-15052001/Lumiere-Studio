"""
Lightweight metadata store for generated images.

Image files themselves keep their existing uuid-based filenames (nothing about
how/where they're saved changes), but every time one is generated we record a
small JSON entry alongside it: the real product name, brand, category, etc.
The /gallery endpoint reads this so the frontend can show and search by an
accurate product name instead of guessing one from the filename.
"""

import json
import os
import threading

STATIC_DIR = "static"
METADATA_PATH = os.path.join(STATIC_DIR, ".metadata.json")
_lock = threading.Lock()


def _load():
    if not os.path.exists(METADATA_PATH):
        return {}
    try:
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def load_metadata():
    """Return the full {filename: {product_name, brand_name, ...}} map."""
    with _lock:
        return _load()


def record_metadata(filename: str, **fields):
    """Upsert metadata for a generated file. None-valued fields are skipped."""
    os.makedirs(STATIC_DIR, exist_ok=True)
    with _lock:
        data = _load()
        entry = data.get(filename, {})
        entry.update({k: v for k, v in fields.items() if v})
        data[filename] = entry
        with open(METADATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def delete_metadata(filename: str):
    with _lock:
        data = _load()
        if filename in data:
            del data[filename]
            with open(METADATA_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)