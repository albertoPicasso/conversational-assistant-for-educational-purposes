from .endCheckerInterface import ChatChecker

## Implementation of LlmInterface using OpenAI API

class NoEndEndChecker(ChatChecker):    

    def checkEndChat(self, message: str) -> bool:
        """
        Checks if the message indicates the end of the chat based on certain levels.

        Args:
        - message (str): The message to be checked for indicating the end of the chat.

        Returns:
        - bool: True if the message contains any of the predefined levels, False otherwise.
        """
        return False