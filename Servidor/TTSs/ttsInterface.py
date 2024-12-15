from abc import ABC, abstractmethod

class TtsInterface(ABC):
    """
    Esta clase base abstracta define la interfaz para la funcionalidad de Texto a Voz (TTS).
    """

    @abstractmethod
    def speak(self, text: str) -> str:
        """
        Convierte texto a voz y reproduce el audio.

        Args:
            text (str): El texto a convertir en voz.

        Returns:
            str: Devuelve la ruta al archivo de audio.
        """
        pass
