import json
import os


CONFIG_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "numan")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "start_on_startup": False,
}


class Config:
    def __init__(self, data=None):
        self._data = data if data is not None else dict(DEFAULT_CONFIG)

    @classmethod
    def load(cls):
        if os.path.isfile(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                merged = dict(DEFAULT_CONFIG)
                merged.update(data)
                return cls(merged)
            except (json.JSONDecodeError, OSError):
                return cls()
        return cls()

    def save(self):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    @property
    def start_on_startup(self):
        return self._data.get("start_on_startup", False)

    @start_on_startup.setter
    def start_on_startup(self, value):
        self._data["start_on_startup"] = bool(value)
