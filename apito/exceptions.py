class InvalidData(Exception):
    def __init__(self, messages: dict):
        if isinstance(messages, dict):
            self.message = messages.get("messages")
        else:
            self.message = messages

        super().__init__(self.message)


class WrongCredentials(Exception):
    pass
