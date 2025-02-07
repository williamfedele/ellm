from dataclasses import dataclass
from datetime import datetime
import tiktoken


def count_tokens(text: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


@dataclass
class Message:
    role: str
    content: str
    timestamp: str = ""
    tokens: int = 0

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if not self.tokens:
            self.tokens = count_tokens(self.content)
