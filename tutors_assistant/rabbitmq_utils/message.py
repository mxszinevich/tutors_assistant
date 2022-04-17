import json
from typing import Optional


class Message:
    """
    Сообщение передаваемое через RabbitMQ
    """
    TYPE_TEXT = "text"
    TYPE_MEDIA = "media"

    def __init__(self,  chat_id: Optional[int] = None, message: str = "", type="text", **extra):
        self.chat_id = chat_id
        self.message = message
        self.type = type
        self.__dict__.update(extra)

    def load_data(self, data: str):
        if isinstance(data, str):
            method = json.loads
        data = json.loads(data)
        if not isinstance(data, dict):
            raise ValueError("Incorrect data")

        self.__dict__.update(data)

    def to_str(self) -> str:
        return json.dumps(self.__dict__)


