from .STTInterface import STTInterface
import os 
import openai as OpenAI 
## Local Implementation of AudioInterface
## Uses the Whisper model from OpenAI locally

class RemoteWhisper(STTInterface):
    """
    This class implements the AudioInterface interface using the Whisper model
    from OpenAI locally.
    """

    ## Constructor
    def __init__(self, model: str, client):
        """
        Initializes the LocalWhisper object.

        Args:
            model_size (str): The Whisper model to use. e.g "whisper-1"
        """
        self.client = client
        self.model = model
        

    def transcribe(self, filename: str) -> str:
        """
        Transcribes an audio file to text using the Whisper model.

        Args:
            filename (str): The path to the audio file to transcribe.

        Returns:
            str: The transcribed text from the audio file.
        """

        # if the request fail throw an exception and will be catched at the top funcion
        #Docu here --- https://platform.openai.com/docs/guides/error-codes
        
        audio_file= open(filename ,"rb")

        transcription = self.client.audio.transcriptions.create(
        model= self.model, 
        file=audio_file
        ) 
        # Return the transcribed text
        return (transcription.text)