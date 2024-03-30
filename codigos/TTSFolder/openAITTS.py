from .ttsInterface import TtsInterface
from openai import OpenAI
import os
from pydub import AudioSegment


class OpenAITTS(TtsInterface):


    def __init__(self, model):
        self.client = OpenAI(api_key=os.getenv("OPENAIKEY"), base_url="https://api.openai.com/v1")
        self.model = model


    def speak(self, text: str) -> str:


        # Define the output filename
        name = "salida.mp3"  
        namewav = "salida.wav"

        # Perform text-to-speech synthesis and save audio
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=self.model,
            input=text,
            response_format="mp3" 
        )  
        
        response.stream_to_file(name)

        #Convert mp3 to wav
        audio = AudioSegment.from_mp3(name)
        audio.export(namewav, format="wav")

        return namewav
    

