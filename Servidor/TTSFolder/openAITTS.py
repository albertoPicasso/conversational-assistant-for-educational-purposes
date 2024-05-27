from .ttsInterface import TtsInterface
from openai import OpenAI
import os
from pydub import AudioSegment


class OpenAITTS(TtsInterface):


    def __init__(self, model):
        self.client = OpenAI(api_key=os.getenv("OPENAIKEY"), base_url="https://api.openai.com/v1")
        self.model = model


    def speak(self, text: str, uid: str) -> str:
        """
        Converts text to speech using the OpenAI TTS model and saves the audio to a file.

        Args:
            text (str): The text to be converted to speech.

        Returns:
            str: The filename of the generated wav audio file.
        """

        # Define the output filename
        name = "salida.mp3"  
        namewav = "salida.wav"
        path = os.path.join(os.getcwd(), "tempUserData", uid, name)
        # Perform text-to-speech synthesis and save audio
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=self.model,
            input=text,
            response_format="mp3" 
        )  
        
        response.stream_to_file(path)

        #Load .mp3 in memory 
        audio = AudioSegment.from_mp3(path)

        path = os.path.join(os.getcwd(), "tempUserData",uid, namewav)
        #Convert mp3 to wav
        audio.export(path, format="wav")

        #remove mp3

        return path
    

