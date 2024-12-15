from abc import ABC, abstractmethod

class TeacherInterface(ABC):
    """
    Esta clase base abstracta define la interfaz para un profesor que evalúa
    mensajes de chat y determina si el chat debe terminar.
    """

    @abstractmethod
    def checkEndChat(self, message: str) -> bool:
        """
        Método abstracto para determinar si un chat debe finalizar basado en un mensaje dado.

        Args:
            message (str): El mensaje recibido en el chat.

        Returns:
            bool: True si el chat debe terminar, False en caso contrario.

        Este método debe ser implementado por cualquier subclase que herede de esta clase.
        """

    @abstractmethod
    def evaluation(self, message_list, last_message, LLM):
        """
        Evalúa y procesa una lista de mensajes, el mensaje más reciente y una instancia de un LLM.

        Este método podría usarse para analizar una secuencia de mensajes de chat, determinar la relevancia
        o respuesta utilizando un modelo de lenguaje (LLM), o realizar otra lógica definida por la implementación específica.

        Args:
            message_list (List[str]): Una lista de todos los mensajes en la sesión de chat.
            last_message (str): El mensaje más reciente en el chat.
            LLM (Any): Una instancia de un modelo de aprendizaje de lenguaje u otra herramienta relacionada. El tipo exacto
                    depende de la implementación y del modelo que se esté utilizando.

        Returns:
            Any: La salida puede variar según el propósito y la lógica del método. Podría ser un nuevo
                mensaje, un resumen, un análisis o cualquier otro tipo de resultado dependiendo de lo que
                'evaluation' esté destinado a lograr en este contexto.
        """
