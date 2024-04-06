from .ttsInterface import TtsInterface
import torch
from TTS.api import TTS
import os 

## CoquiTTS Implementation for Text-to-Speech (TTS)

class CoquiTTS(TtsInterface):
    """
    This class implements the TtsInterface for Text-to-Speech (TTS) functionality 
    using the Coqui TTS library.

    It takes a TTS model name as an argument in the constructor and uses the 
    Coqui TTS API to convert text to speech and save the generated audio to a file.
    """

    def __init__(self, model):
        """
        Initializes the CoquiTTS object.

        Args:
            model (str): The name of the Coqui TTS model to use (e.g., "tts_models/en/ljspeech").
        """

        # Automatically configure device (CPU or GPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load the Coqui TTS model onto the chosen device
        self.model = model
        self.TTS = TTS(model_name=self.model).to(self.device)

    def speak(self, text: str, uid: str) -> str:
        """
        Converts text to speech using the Coqui TTS model and saves the audio to a file.

        Args:
            text (str): The text to be converted to speech.

        Returns:
            str: The filename of the generated wav audio file.
        """
        # if the request fail throw an exception and will be catched at the top funcion
        # Define the output filename
        name = "output.wav"  
        path = os.path.join(os.getcwd(), uid, name)
        # Perform text-to-speech synthesis and save audio
        self.TTS.tts_to_file(text=text, file_path=path, speed=1.2, split_sentences=False)

        # Return the filename of the generated audio
        return path
