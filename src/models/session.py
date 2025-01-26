from uuid import uuid4
from utils.constants import HISTORY_PATH
import json
import utils.prompts as prompts
from models.message import Message
from dataclasses import asdict
from datetime import datetime


class Session:
    def __init__(self, id: str = None):
        self.id = id or str(uuid4())
        self.title: str = "Untitled"
        self.settings = "DEFAULT"
        self.history_file = HISTORY_PATH / f"{self.id}.json"
        self.history: List[Message] = []
        self.created_at = datetime.now().isoformat()
        if id:
            self.load_history()
        else:
            self.history.append(Message(role="system", content=prompts.chat))

    def load_history(self) -> None:
        if self.history_file.exists():
            with open(self.history_file) as f:
                data = json.load(f)
                self.title = data.get("title", "Untitled")
                self.settings = data.get("settings", "DEFAULT")
                self.created_at = data.get("created_at", self.created_at)
                self.history = [Message(**msg) for msg in data.get("history", [])]

    def save_history(self) -> None:
        data = {
            "title": self.title,
            "settings": self.settings,
            "created_at": self.created_at,
            "history": [asdict(msg) for msg in self.history],
        }
        with open(self.history_file, "w") as f:
            json.dump(data, f, indent=2)

    def add_message(self, role: str, content: str) -> None:
        message = Message(role=role, content=content)
        self.history.append(message)
        self.save_history()

    def get_token_count(self):
        return sum(msg.tokens for msg in self.history)
