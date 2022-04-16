import json
from typing import Optional


class Message:
    """
    Сообщение передаваемое через RabbitMQ
    """

    def __init__(self,  chat_id: Optional[int] = None, message: str = "", data: Optional[str] = None):
        if data:
            data = json.loads(data)
            if not isinstance(data, dict):
                raise ValueError("Incorrect data")
            self.__dict__.update(data)
        else:
            self.chat_id = chat_id
            self.message = message

    def to_str(self) -> str:
        return json.dumps(self.__dict__)


