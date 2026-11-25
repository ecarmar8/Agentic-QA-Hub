import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))
EXPORT_DIR = BASE_DIR / "exports"
STATIC_DIR = BASE_DIR / "app" / "static"
SKILLS_DIR = BASE_DIR / "skills"
AI_PROVIDER = os.getenv("AI_PROVIDER", "local").lower()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-7-sonnet-latest")
APP_SECRET = os.getenv("APP_SECRET", "development-only-change-me")

DATA_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
