from abc import ABC, abstractmethod

## Interfaz dedicada al manejo de reconocimiento de voz a texto (STT)
## Proporciona métodos abstractos

class STTInterface(ABC):
    """
    Esta clase base abstracta define la interfaz para transcribir archivos de audio.
    """

    @abstractmethod
    def transcribe(self, filename: str) -> str:
        """
        Transcribe un archivo de audio a texto.

        Args:
            filename (str): La ruta al archivo de audio a transcribir.

        Returns:
            str: El texto transcrito del archivo de audio.
        """
        pass
