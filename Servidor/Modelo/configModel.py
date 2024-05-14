class ConfigModel:
    def __init__(self):
        self._language = "es"
        self._stt = "local"
        self._whisper_size = "small"
        self._llm = "local"
        self._llm_models = "gemma"
        self._tts = "local"
        self._port = "5000"

    # Getter and Setter for language
    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        self._language = value

    # Getter and Setter for stt
    @property
    def stt(self):
        return self._stt

    @stt.setter
    def stt(self, value):
        self._stt = value

    # Getter and Setter for whisper_size
    @property
    def whisper_size(self):
        return self._whisper_size

    @whisper_size.setter
    def whisper_size(self, value):
        self._whisper_size = value

    # Getter and Setter for llm
    @property
    def llm(self):
        return self._llm

    @llm.setter
    def llm(self, value):
        self._llm = value

    # Getter and Setter for llm_models
    @property
    def llm_models(self):
        return self._llm_models

    @llm_models.setter
    def llm_models(self, value):
        self._llm_models = value

    # Getter and Setter for tts
    @property
    def tts(self):
        return self._tts

    @tts.setter
    def tts(self, value):
        self._tts = value

    # Getter and Setter for port
    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value


