from .STTInterface import STTInterface
import os 
import openai as OpenAI

## Implementación remota de AudioInterface
## Utiliza el modelo Whisper de OpenAI de forma remota

class RemoteWhisper(STTInterface):
    """
    Esta clase implementa la interfaz AudioInterface utilizando el modelo Whisper
    de OpenAI de forma remota.
    """

    ## Constructor
    def __init__(self, model: str, client):
        """
        Inicializa el objeto RemoteWhisper.

        Args:
            model (str): El modelo Whisper a utilizar, por ejemplo "whisper-1".
            client (OpenAI): El cliente de OpenAI utilizado para interactuar con la API.
        """
        self.client = client
        self.model = model

    def transcribe(self, filename: str) -> str:
        """
        Transcribe un archivo de audio a texto usando el modelo Whisper.

        Args:
            filename (str): La ruta al archivo de audio a transcribir.

        Returns:
            str: El texto transcrito del archivo de audio.
        """

        # Si la solicitud falla, lanzará una excepción que será capturada en la función superior
        # Documentación aquí: https://platform.openai.com/docs/guides/error-codes
        
        audio_file = open(filename, "rb")

        transcription = self.client.audio.transcriptions.create(
            model=self.model, 
            file=audio_file
        ) 
        # Devolver el texto transcrito
        return (transcription.text)
