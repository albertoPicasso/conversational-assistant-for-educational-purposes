from abc import ABC, abstractmethod

class LlmInterface(ABC):
    """
    Esta clase base abstracta define la interfaz para interactuar con modelos 
    de lenguaje grande (LLMs).
    """

    @abstractmethod
    def request_to_llm(self, chat) -> str:
        """
        Envía una solicitud a un LLM.

        Args:
            chat (str): El texto a enviar al LLM.

        Returns:
            str: La respuesta del LLM. SOLO CADENA, NO JSON COMPLETO
        """
        pass
