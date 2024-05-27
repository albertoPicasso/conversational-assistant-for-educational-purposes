from .llmInterface import LlmInterface

## Implementación de LlmInterface usando la API de OpenAI

class OpenAIAPI(LlmInterface):
    """
    Esta clase implementa LlmInterface para interactuar con la API de OpenAI.

    Toma un objeto cliente de OpenAI y un nombre de modelo LLM como argumentos en el 
    constructor. El método `request_to_llm` envía una solicitud de chat al modelo 
    especificado usando el cliente de OpenAI y devuelve la respuesta.
    """

    def __init__(self, client, model):
        """
        Inicializa el objeto OpenAIAPI.

        Args:
            client (OpenAI): Un objeto cliente de OpenAI utilizado para interactuar con la API.
            model (str): El nombre del modelo LLM de OpenAI a usar (por ejemplo, "text-davinci-003").
        """
        self.model = model
        self.client = client

    def request_to_llm(self, chat, temp=1) -> str:
        """
        Envía una solicitud de chat al LLM de OpenAI y devuelve la respuesta.

        Args:
            chat (list): El texto a enviar al LLM en formato de lista de tuplas (rol, contenido).
            temp (float): La temperatura para la generación del texto (opcional, por defecto es 1).

        Returns:
            str: La respuesta del LLM.
        """
        # Crear un array de mensajes para hacer una solicitud con el formato [{"role": rol, "content": contenido}]
        request_messages = []
        for message in chat: 
            request_messages.append({"role": message[0], "content": message[1]})

        # Solicitar al modelo
        chat_completion = self.client.chat.completions.create(
            messages=request_messages,
            model=self.model,
            temperature=temp
        )

        # Si la solicitud falla, se lanzará una excepción que será capturada en la función superior
        # Documentación aquí: https://platform.openai.com/docs/guides/error-codes
        return chat_completion.choices[0].message.content
