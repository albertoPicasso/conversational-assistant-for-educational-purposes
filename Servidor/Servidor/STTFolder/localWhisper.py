import whisper
import torch
from .STTInterface import STTInterface

## Implementación local de AudioInterface
## Utiliza el modelo Whisper de OpenAI localmente

class LocalWhisper(STTInterface):
    """
    Esta clase implementa la interfaz AudioInterface utilizando el modelo Whisper
    de OpenAI localmente.
    """

    ## Constructor
    def __init__(self, model_size: str) -> None:
        """
        Inicializa el objeto LocalWhisper.

        Args:
            model_size (str): El tamaño del modelo Whisper a utilizar. Puede ser
                "small", "base" o "tiny"; no se pueden usar modelos más grandes debido a limitaciones de VRAM.
        """
        self.model = model_size
        # Configura automáticamente el dispositivo (CPU o GPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        

    def transcribe(self, filename: str) -> str:
        """
        Transcribe un archivo de audio a texto usando el modelo Whisper.

        Args:
            filename (str): La ruta al archivo de audio a transcribir.

        Returns:
            str: El texto transcrito del archivo de audio.
        """
        
        # Si algo falla, lanzará una excepción que será capturada a nivel superior
        # Cargar el modelo Whisper en el dispositivo elegido (CPU o GPU)
        model = whisper.load_model(self.model, self.device)

        # Transcribir el archivo de audio
        result = model.transcribe(audio=filename, no_speech_threshold=1.5)

        # Devolver el texto transcrito
        return result["text"]
