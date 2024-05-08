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



    def evaluation(self, message_list, last_message, LLM):
        """
        Evaluate and process a list of messages, the most recent message, and an LLM instance.

        This method could be used to analyze a sequence of chat messages, determine the relevance 
        or response using a language model (LLM), or perform other logic defined by the specific 
        implementation.

        Args:
            message_list (List[str]): A list of all messages in the chat session.
            last_message (str): The most recent message in the chat.
            LLM (Any): An instance of a language learning model or related tool. The exact type 
                    depends on the implementation and the model being used.

        Returns:
            Any: The output can vary based on the method's purpose and logic. It could be a new 
                message, a summary, an analysis, or any other type of result depending on what 
                'evaluation' is meant to achieve in this context.
        """
