from abc import ABC, abstractmethod

class TtsInterface(ABC):
    """
    This abstract base class defines the interface for Text-to-Speech (TTS) functionality.
    """

    @abstractmethod
    def speak(self, text: str) -> str:
        """
        Converts text to speech and plays the audio.

        Args:
            text (str): The text to be converted to speech.

        Returns:
            (str): Return the path to audio.
        """
        pass
