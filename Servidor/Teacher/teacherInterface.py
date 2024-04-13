from abc import ABC, abstractmethod

class TeacherInterface(ABC):
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

    @abstractmethod
    def evaluation(self, message_list, last_message, LLM):
        pass