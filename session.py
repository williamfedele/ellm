from uuid import uuid4
from constants import HISTORY_PATH
import json
import prompts


class Session:
    def __init__(self, id: str = None):
        self.id = id or str(uuid4())
        self.history_file = HISTORY_PATH / f"{self.id}.json"
        self.history: List[Dict] = []
        if id:
            self.load_history()
        else:
            self.history.append({"role": "system", "content": prompts.chat})

    def load_history(self) -> None:
        if self.history_file.exists():
            with open(self.history_file) as f:
                self.history = json.load(f)

    def save_history(self) -> None:
        with open(self.history_file, "w") as f:
            json.dump(self.history, f, indent=2)

    def add_message(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})
        self.save_history()
