from .endCheckerInterface import ChatChecker

## Implementation of LlmInterface using OpenAI API

class TeacherEndChecker(ChatChecker):    

    def checkEndChat(self, message: str) -> bool:
        """
        Checks if the message indicates the end of the chat based on certain levels.

        Args:
        - message (str): The message to be checked for indicating the end of the chat.

        Returns:
        - bool: True if the message contains any of the predefined levels, False otherwise.
        """
        levels = ["A1","A2","B1","B2","C1","C2", "[END]"]
        for level in levels: 
            if level in message:
                return True
        
        return False 
