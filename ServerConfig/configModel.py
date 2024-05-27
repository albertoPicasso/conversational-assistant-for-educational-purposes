class ConfigModel:
    """
    Class for storing and managing the server configuration settings.

    This class provides getters and setters for various configuration
    settings such as language, STT, Whisper model size, LLM, LLM models,
    TTS, and port.
    """

    def __init__(self):
        """
        Initializes an instance of the ConfigModel class with default settings.
        """
        self._language = "es"
        self._stt = "local"
        self._whisper_size = "small"
        self._llm = "local"
        self._llm_models = "gemma"
        self._tts = "local"
        self._port = "5000"

    @property
    def language(self):
        """
        Get the current language setting.

        Returns:
            str: The current language setting.
        """
        return self._language

    @language.setter
    def language(self, value):
        """
        Set a new language.

        Args:
            value (str): The new language to set.
        """
        self._language = value

    @property
    def stt(self):
        """
        Get the current speech-to-text (STT) setting.

        Returns:
            str: The current STT setting.
        """
        return self._stt

    @stt.setter
    def stt(self, value):
        """
        Set a new speech-to-text (STT) setting.

        Args:
            value (str): The new STT setting to set.
        """
        self._stt = value

    @property
    def whisper_size(self):
        """
        Get the current Whisper model size setting.

        Returns:
            str: The current Whisper model size setting.
        """
        return self._whisper_size

    @whisper_size.setter
    def whisper_size(self, value):
        """
        Set a new Whisper model size.

        Args:
            value (str): The new Whisper model size to set.
        """
        self._whisper_size = value

    @property
    def llm(self):
        """
        Get the current large language model (LLM) setting.

        Returns:
            str: The current LLM setting.
        """
        return self._llm

    @llm.setter
    def llm(self, value):
        """
        Set a new large language model (LLM) setting.

        Args:
            value (str): The new LLM setting to set.
        """
        self._llm = value

    @property
    def llm_models(self):
        """
        Get the current LLM models setting.

        Returns:
            str: The current LLM models setting.
        """
        return self._llm_models

    @llm_models.setter
    def llm_models(self, value):
        """
        Set new LLM models.

        Args:
            value (str): The new LLM models to set.
        """
        self._llm_models = value

    @property
    def tts(self):
        """
        Get the current text-to-speech (TTS) setting.

        Returns:
            str: The current TTS setting.
        """
        return self._tts

    @tts.setter
    def tts(self, value):
        """
        Set a new text-to-speech (TTS) setting.

        Args:
            value (str): The new TTS setting to set.
        """
        self._tts = value

    @property
    def port(self):
        """
        Get the current port setting.

        Returns:
            int: The current port setting.
        """
        return self._port

    @port.setter
    def port(self, value):
        """
        Set a new port.

        Args:
            value (int): The new port setting to set.
        """
        self._port = value
