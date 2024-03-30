from .llmInterface import LlmInterface

## Implementation of LlmInterface using OpenAI API

class OpenAIAPI(LlmInterface):
    """
    This class implements the LlmInterface for interacting with the OpenAI API.

    It takes an OpenAI client object and an LLM model name as arguments in the 
    constructor. The `request_to_llm` method sends a chat request to the specified 
    model using the OpenAI client and returns the response.
    """

    def __init__(self, client, model):
        """
        Initializes the OpenAIAPI object.

        Args:
            client (OpenAI): An OpenAI client object used for interacting with the API.
            model (str): The name of the OpenAI LLM model to use (e.g., "text-davinci-003").
        """
        self.model = model
        self.client = client

    def request_to_llm(self, chat) -> str:
        """
        Sends a chat request to the OpenAI LLM and returns the response.

        Args:
            chat (str): The text to send to the LLM.

        Returns:
            str : The LLM response
        """
        chat_completion = self.client.chat.completions.create(
            messages= chat,
            model=self.model,
        )

        return chat_completion.choices[0].message.content
