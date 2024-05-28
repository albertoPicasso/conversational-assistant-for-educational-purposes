from .ttsInterface import TtsInterface
import torch
from TTS.api import TTS
import os 

## Implementación de CoquiTTS para Texto a Voz (TTS)

class CoquiTTS(TtsInterface):
    """
    Esta clase implementa la interfaz TtsInterface para la funcionalidad de Texto a Voz (TTS)
    utilizando la biblioteca Coqui TTS.

    Toma el nombre de un modelo TTS como argumento en el constructor y utiliza
    la API de Coqui TTS para convertir texto a voz y guardar el audio generado en un archivo.
    """

    def __init__(self, model):
        """
        Inicializa el objeto CoquiTTS.

        Args:
            model (str): El nombre del modelo Coqui TTS a utilizar (por ejemplo, "tts_models/en/ljspeech").
        """
        # Configura automáticamente el dispositivo (CPU o GPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Cargar el modelo Coqui TTS en el dispositivo elegido
        self.model = model
        self.TTS = TTS(model_name=self.model).to(self.device)

    def speak(self, text: str, uid: str) -> str:
        """
        Convierte texto a voz utilizando el modelo Coqui TTS y guarda el audio en un archivo.

        Args:
            text (str): El texto a convertir en voz.
            uid (str): El identificador de usuario para crear una ruta única para el archivo de audio.

        Returns:
            str: El nombre del archivo de audio generado en formato wav.
        """
        # Si la solicitud falla, lanzará una excepción que será capturada en la función superior
        # Definir el nombre del archivo de salida
        nombre = "output.wav"  
        ruta = os.path.join(os.getcwd(), "tempUserData", uid, nombre)
        
        # Realizar la síntesis de texto a voz y guardar el audio
        self.TTS.tts_to_file(text=text, file_path=ruta, speed=1.2, split_sentences=False)

        # Devolver el nombre del archivo de audio generado
        return ruta
