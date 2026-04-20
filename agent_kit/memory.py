from agent_kit.types import Message


class Memory:
    def __init__(self, initial_context=None):
        self.context = [*(initial_context or [])]

    def is_empty(self):
        return len(self.context) < 1

    def add_message(self, message: Message):
        self.context.append(message)

    def get_context(self):
        return self.context.copy()
