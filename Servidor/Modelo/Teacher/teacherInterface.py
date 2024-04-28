from abc import ABC, abstractmethod

class TeacherInterface(ABC):
    
    def checkEndChat(self, message: str) -> bool:
        """
        Abstract method to determine if a chat should end based on a given message.

        Args:
            message (str): The message received in the chat.

        Returns:
            bool: True if the chat should end, False otherwise.

        This method must be implemented by any subclass that inherits from this class.
        """



    def evaluation(self, message_list, last_message, LLM) -> str:
        """
        Abstract method to determine the statement.

        Args:
            message List(str): The messages of the chat.
            last_message (str): Last message

        Returns:
            str: Evaluation

        This method must be implemented by any subclass that inherits from this class.
        """