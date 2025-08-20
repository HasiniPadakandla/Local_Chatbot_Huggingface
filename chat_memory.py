class ChatMemory:
    def __init__(self, max_turns: int = 5):
        self.max_turns = max_turns
        self.history = []

    def append(self, user_input: str, bot_reply: str):
        self.history.append((user_input, bot_reply))
        if len(self.history) > self.max_turns:
            self.history.pop(0)

    def get_context(self) -> str:
        """
        Construct conversation context string from history.
        """
        context = ""
        for user, bot in self.history:
            context += f"User: {user}\nBot: {bot}\n"
        return context
