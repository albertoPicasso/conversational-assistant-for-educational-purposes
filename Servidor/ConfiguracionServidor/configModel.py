class ConfigModel:
    """
    Clase para almacenar y gestionar las configuraciones del servidor.

    Esta clase proporciona getters y setters para varias configuraciones
    tales como idioma, STT, tamaño del modelo Whisper, LLM, modelos LLM,
    TTS y puerto.
    """

    def __init__(self):
        """
        Inicializa una instancia de la clase ConfigModel con configuraciones por defecto.
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
        Obtiene la configuración actual del idioma.

        Returns:
            str: La configuración actual del idioma.
        """
        return self._language

    @language.setter
    def language(self, value):
        """
        Establece un nuevo idioma.

        Args:
            value (str): El nuevo idioma a establecer.
        """
        self._language = value

    @property
    def stt(self):
        """
        Obtiene la configuración actual del servicio de reconocimiento de voz (STT).

        Returns:
            str: La configuración actual de STT.
        """
        return self._stt

    @stt.setter
    def stt(self, value):
        """
        Establece una nueva configuración para el servicio de reconocimiento de voz (STT).

        Args:
            value (str): La nueva configuración de STT a establecer.
        """
        self._stt = value

    @property
    def whisper_size(self):
        """
        Obtiene la configuración actual del tamaño del modelo Whisper.

        Returns:
            str: La configuración actual del tamaño del modelo Whisper.
        """
        return self._whisper_size

    @whisper_size.setter
    def whisper_size(self, value):
        """
        Establece un nuevo tamaño para el modelo Whisper.

        Args:
            value (str): El nuevo tamaño del modelo Whisper a establecer.
        """
        self._whisper_size = value

    @property
    def llm(self):
        """
        Obtiene la configuración actual del modelo de lenguaje grande (LLM).

        Returns:
            str: La configuración actual de LLM.
        """
        return self._llm

    @llm.setter
    def llm(self, value):
        """
        Establece una nueva configuración para el modelo de lenguaje grande (LLM).

        Args:
            value (str): La nueva configuración de LLM a establecer.
        """
        self._llm = value

    @property
    def llm_models(self):
        """
        Obtiene la configuración actual de los modelos LLM.

        Returns:
            str: La configuración actual de los modelos LLM.
        """
        return self._llm_models

    @llm_models.setter
    def llm_models(self, value):
        """
        Establece nuevos modelos LLM.

        Args:
            value (str): Los nuevos modelos LLM a establecer.
        """
        self._llm_models = value

    @property
    def tts(self):
        """
        Obtiene la configuración actual del servicio de texto a voz (TTS).

        Returns:
            str: La configuración actual de TTS.
        """
        return self._tts

    @tts.setter
    def tts(self, value):
        """
        Establece una nueva configuración para el servicio de texto a voz (TTS).

        Args:
            value (str): La nueva configuración de TTS a establecer.
        """
        self._tts = value

    @property
    def port(self):
        """
        Obtiene la configuración actual del puerto.

        Returns:
            int: La configuración actual del puerto.
        """
        return self._port

    @port.setter
    def port(self, value):
        """
        Establece un nuevo puerto.

        Args:
            value (int): La nueva configuración de puerto a establecer.
        """
        self._port = value
