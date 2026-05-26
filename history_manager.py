import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"

def load_history():
    """Load history from JSON file."""
    if not os.path.exists(HISTORY_FILE):
        return {"liked": [], "recent": []}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"liked": [], "recent": []}

def save_history(history):
    """Save history to JSON file."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def add_to_history(job_description: str, title: str):
    """Add a new search to recent history."""
    history = load_history()

    history["recent"] = [
        h for h in history["recent"]
        if h["job_description"] != job_description
    ]

    history["recent"].insert(0, {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "title": title,
        "job_description": job_description,
        "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p")
    })

    history["recent"] = history["recent"][:5]

    save_history(history)
    return history

def toggle_like(item_id: str):
    """Like or unlike a history item."""
    history = load_history()

    liked_ids = [h["id"] for h in history["liked"]]

    if item_id in liked_ids:
        history["liked"] = [h for h in history["liked"] if h["id"] != item_id]
    else:
        if len(history["liked"]) >= 3:
            return history, "⚠️ Max 3 liked items. Unlike one first!"

        item = next((h for h in history["recent"] if h["id"] == item_id), None)
        if item:
            history["liked"].append(item)

    save_history(history)
    return history, "ok"

def get_all_history():
    """Return liked (top) + recent (bottom, excluding liked)."""
    history = load_history()
    liked = history.get("liked", [])
    recent = history.get("recent", [])

    liked_ids = {h["id"] for h in liked}
    recent_filtered = [h for h in recent if h["id"] not in liked_ids]

    return liked, recent_filtered