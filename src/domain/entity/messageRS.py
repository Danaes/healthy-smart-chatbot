from enum import Enum


class MessageType(Enum):
    TEXT = 0
    FILE = 1


class MessageRS:

    def __init__(self, text, type_message):
        self.text = text
        self.type = type_message

    def __len__(self):
        return len(self.text)
