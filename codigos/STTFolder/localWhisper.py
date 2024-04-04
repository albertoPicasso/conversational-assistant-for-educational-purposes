import whisper
import torch
from .audioInterface import AudioInterface

## Local Implementation of AudioInterface
## Uses the Whisper model from OpenAI locally

class LocalWhisper(AudioInterface):
    """
    This class implements the AudioInterface interface using the Whisper model
    from OpenAI locally.
    """

    ## Constructor
    def __init__(self, model_size: str) -> None:
        """
        Initializes the LocalWhisper object.

        Args:
            model_size (str): The size of the Whisper model to use. This can be
                "small", "base", or "tiny" cannot use larger models due to vram limitation
        """
        self.model = model_size
        # Automatically configure device (CPU or GPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        

    def transcribe(self, filename: str) -> str:
        """
        Transcribes an audio file to text using the Whisper model.

        Args:
            filename (str): The path to the audio file to transcribe.

        Returns:
            str: The transcribed text from the audio file.
        """
        
        #If something flails trhow an exception that will be catched a top level
        # Load the Whisper model onto the chosen device (CPU or GPU)
        model = whisper.load_model(self.model, self.device)

        # Transcribe the audio file
        result = model.transcribe(audio=filename)
        

        # Return the transcribed text
        return result["text"]