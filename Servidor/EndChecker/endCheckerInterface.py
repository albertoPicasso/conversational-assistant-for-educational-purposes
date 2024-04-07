from abc import ABC, abstractmethod

class ChatChecker(ABC):
    @abstractmethod
    def checkEndChat(self, message: str) -> bool:
        """
        Abstract method to determine if a chat should end based on a given message.

        Args:
            message (str): The message received in the chat.

        Returns:
            bool: True if the chat should end, False otherwise.

        This method must be implemented by any subclass that inherits from this class.
        """
        pass
