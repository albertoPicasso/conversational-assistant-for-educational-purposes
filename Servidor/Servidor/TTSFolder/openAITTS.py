from .ttsInterface import TtsInterface
from openai import OpenAI
import os
from pydub import AudioSegment

class OpenAITTS(TtsInterface):
    """
    Esta clase implementa la interfaz TtsInterface utilizando el modelo TTS de OpenAI.
    """

    def __init__(self, model):
        """
        Inicializa el objeto OpenAITTS.

        Args:
            model (str): El modelo de voz de OpenAI a utilizar.
        """
        self.client = OpenAI(api_key=os.getenv("OPENAIKEY"), base_url="https://api.openai.com/v1")
        self.model = model

    def speak(self, text: str, uid: str) -> str:
        """
        Convierte texto a voz utilizando el modelo TTS de OpenAI y guarda el audio en un archivo.

        Args:
            text (str): El texto a convertir en voz.
            uid (str): El identificador de usuario para crear una ruta única para el archivo de audio.

        Returns:
            str: El nombre del archivo de audio generado en formato wav.
        """
        # Definir el nombre del archivo de salida
        name = "salida.mp3"  
        namewav = "salida.wav"
        path = os.path.join(os.getcwd(), "tempUserData", uid, name)
        
        # Realizar la síntesis de texto a voz y guardar el audio
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=self.model,
            input=text,
            response_format="mp3"
        )
        
        response.stream_to_file(path)

        # Cargar el archivo .mp3 en memoria
        audio = AudioSegment.from_mp3(path)

        path_wav = os.path.join(os.getcwd(), "tempUserData", uid, namewav)
        # Convertir mp3 a wav
        audio.export(path_wav, format="wav")

        # Devolver la ruta del archivo wav
        return path_wav
