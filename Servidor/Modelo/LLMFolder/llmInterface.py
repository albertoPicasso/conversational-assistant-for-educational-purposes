from abc import ABC, abstractmethod

class LlmInterface(ABC):
    """
    This abstract base class defines the interface for interacting with large 
    language models (LLMs).
    """

    
    def request_to_llm(self, chat) -> str:
        """
        Sends a request to a llm.

        Args:
            chat (str): The text to send to the LLM.

        Returns:
            str: The response from the LLM. ONLY STRING NO COMPLETE JSON 
        """
    
