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

    def request_to_llm(self, chat, temp = 1) -> str:
        """
        Sends a chat request to the OpenAI LLM and returns the response.

        Args:
            chat (str): The text to send to the LLM.

        Returns:
            str : The LLM response
        """
        # Create messages array to make a request with format ["role": rolemessage , "content": contentmessage }]
        request_messages = []
        for message in chat: 
            request_messages.append({"role": message[0], "content": message[1]})

        #ask model
        chat_completion = self.client.chat.completions.create(
            messages= request_messages,
            model=self.model,
            temperature=temp
        )
        # if the request fail throw an exception and will be catched at the top funcion
        #Docu here --- https://platform.openai.com/docs/guides/error-codes
        return chat_completion.choices[0].message.content
