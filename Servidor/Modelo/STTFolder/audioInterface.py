from abc import ABC, abstractmethod

## Interface dedicated to Speech-to-Text (STT) handling
## Provides abstract methods 

class AudioInterface(ABC):
    """
    This abstract base class defines the interface for transcribing audio files.
    """

    
    def transcribe(self, filename: str) -> str:
        """
        Transcribes an audio file to text.

        Args:
            filename (str): The path to the audio file to transcribe.

        Returns:
            str: The transcribed text from the audio file.
        """
        
