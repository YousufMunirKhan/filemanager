"""Reads backend/.env before the app starts.

Kept outside the `app` package on purpose: importing `app` reads the settings, so this must run first.
It forgives the usual mistakes made when copying settings to another laptop:
- the file is in the project folder, or saved as ".env.txt" by Notepad / TextEdit;
- settings were pasted above the empty template lines (normally the last, empty line would win);
- there are two .env files and the filled-in values are in the other one.
"""
import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
# In order of priority: backend/.env is the right place.
CANDIDATES = (BACKEND_DIR / ".env", BACKEND_DIR.parent / ".env", BACKEND_DIR / ".env.txt")
TEMPLATE = BACKEND_DIR / ".env.example"


def read_pairs(path: Path) -> list[tuple[str, str]]:
    """Every KEY=value line of one file, in order (repeated keys included)."""
    from dotenv.parser import parse_stream

    with open(path, encoding="utf-8-sig") as stream:
        return [(b.key, b.value or "") for b in parse_stream(stream) if b.key and not b.error]


def merged_settings(files, defaults: dict[str, str] | None = None) -> dict[str, str]:
    """Choose one value per setting when it is written more than once.

    A value someone typed in beats a value copied unchanged from .env.example (`defaults`), which beats
    an empty one - wherever the lines are. So pasting real settings above or below the template lines
    both work. A tie goes to the last line inside a file, and to the earlier (higher-priority) file.
    """
    defaults = defaults or {}

    def rank(key: str, value: str) -> int:
        if not value.strip():
            return 0
        return 1 if value == defaults.get(key) else 2

    merged: dict[str, str] = {}
    for path in files:
        values: dict[str, str] = {}
        for key, value in read_pairs(path):
            if key not in values or rank(key, value) >= rank(key, values[key]):
                values[key] = value
        for key, value in values.items():
            if key not in merged or rank(key, value) > rank(key, merged[key]):
                merged[key] = value
    return merged


def load_settings(candidates=CANDIDATES, template=TEMPLATE) -> list[Path]:
    """Put the settings into the environment and return the files that were read.

    `flask run` has already loaded backend/.env by itself, the plain way (the last line wins, even an
    empty template line). Values that came from a file like that are replaced by the better choice;
    a real environment variable (not found in any file) is kept.
    """
    from dotenv import dotenv_values

    files = [path for path in candidates if path.is_file()]
    defaults = dict(read_pairs(template)) if template.is_file() else {}
    from_files: dict[str, set[str]] = {}  # what a plain .env loader may already have put in the environment
    for path in files:
        for key, value in dotenv_values(path, encoding="utf-8-sig").items():
            from_files.setdefault(key, set()).add(value or "")
    for key, value in merged_settings(files, defaults).items():
        current = os.environ.get(key)
        if current is None or not current.strip() or current in from_files.get(key, ()):
            os.environ[key] = value
    return files
