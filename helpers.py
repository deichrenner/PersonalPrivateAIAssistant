import dataclasses
import json
from pathlib import Path
from typing import List


@dataclasses.dataclass
class Message:
    message_text: str
    message_id: str
    timestamp: str


def store_messages(file_path: Path, data: List[Message]):
    with file_path.open("w") as f:
        json.dump([dataclasses.asdict(message) for message in data], f)


def load_messages(file_path: Path) -> List[Message]:
    if not file_path.exists():
        return []
    with file_path.open("r") as f:
        return [Message(**message) for message in json.load(f)]
