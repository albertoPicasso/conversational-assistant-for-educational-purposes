from .teacherInterface import TeacherInterface

## Implementation of LlmInterface using OpenAI API

class NoTeacher(TeacherInterface):    

    def checkEndChat(self, message: str) -> bool:
        """
        Return False for no limits chats

        Args:
        - message (str): The message to be checked for indicating the end of the chat.

        Returns:
        - bool: False
        """
        return False
    
    
    def evaluation(self, message_list, last_message, LLM):
        """
        Evaluates the provided messages and returns the last message.

        This function takes a list of messages, the last message in the list, and a language model, then returns the last message.

        Args:
        - message_list (list): A list of messages to evaluate.
        - last_message (str): The last message in the list.
        - LLM (object): The language model to use for evaluation.

        Returns:
        - str: The last message in the list.
        """
        return last_message


