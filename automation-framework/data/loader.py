import csv
import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).parent


def load_json(filename: str) -> Any:
    file_path = DATA_DIR / filename
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def load_csv(filename: str) -> list[dict[str, str]]:
    file_path = DATA_DIR / filename
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [{k.strip(): (v or "").strip() for k, v in row.items()} for row in reader]


def get_user_from_csv(description: str) -> dict[str, str] | None:
    users = load_csv("users.csv")
    return next((u for u in users if u.get("description") == description), None)
