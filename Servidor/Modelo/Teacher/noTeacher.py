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
        return last_message


