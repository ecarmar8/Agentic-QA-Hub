import json
from pathlib import Path
from threading import RLock
from datetime import datetime, timezone
from uuid import uuid4
from app.core.config import DATA_DIR

_lock = RLock()
DB_FILE = DATA_DIR / "store.json"

DEFAULT = {"reviews": [], "runs": [], "audit": []}

def _load():
    if not DB_FILE.exists():
        return DEFAULT.copy()
    try:
        return json.loads(DB_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return DEFAULT.copy()

def _save(data):
    tmp = DB_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(DB_FILE)

def now():
    return datetime.now(timezone.utc).isoformat()

def add_run(agent, title, payload):
    with _lock:
        db = _load()
        item = {"id": str(uuid4()), "agent": agent, "title": title, "payload": payload, "created_at": now()}
        db["runs"].insert(0, item)
        _save(db)
        return item

def add_review(agent, title, content):
    with _lock:
        db = _load()
        item = {"id": str(uuid4()), "agent": agent, "title": title, "content": content,
                "status": "pending", "reviewer_note": "", "created_at": now(), "reviewed_at": None}
        db["reviews"].insert(0, item)
        _save(db)
        return item

def list_reviews():
    return _load()["reviews"]

def review_item(item_id, status, note=""):
    with _lock:
        db = _load()
        for item in db["reviews"]:
            if item["id"] == item_id:
                item["status"] = status
                item["reviewer_note"] = note
                item["reviewed_at"] = now()
                _save(db)
                return item
    return None

def list_runs():
    return _load()["runs"]

def audit(action, actor="local-user", details=None):
    with _lock:
        db = _load()
        event = {"id": str(uuid4()), "action": action, "actor": actor, "details": details or {}, "created_at": now()}
        db["audit"].insert(0, event)
        db["audit"] = db["audit"][:5000]
        _save(db)
        return event

def list_audit():
    return _load()["audit"]
