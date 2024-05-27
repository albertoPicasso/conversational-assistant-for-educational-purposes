import sys
import os
# ..from Servidor.Modelo.serverMain import Servidor
from configModel import ConfigModel


class ConfigController: 
    """
    Clase controladora para la gestión de la configuración del servidor.

    Esta clase maneja la lógica para gestionar y actualizar la configuración del servidor, tales como 
    el idioma, el servicio de reconocimiento de voz (STT), el modelo de lenguaje grande (LLM), 
    el servicio de texto a voz (TTS), el tamaño del modelo Whisper y el puerto del servidor. 
    Interactúa con el modelo para recuperar y establecer estas configuraciones.
    """
    def __init__(self):
        """
        Inicializa la aplicación principal.

        Este constructor realiza las siguientes acciones:
        - Agrega el directorio de trabajo actual al path del sistema.
        - Agrega el path del módulo específico al path del sistema si aún no está presente.
        - Importa la clase `Servidor` del módulo `serverMain`.
        - Inicializa una instancia de la clase `Servidor` y la asigna a `self.serverModel`.
        - Inicializa una instancia de la clase `ConfigModel` y la asigna a `self.model`.

        Atributos:
            serverModel (Servidor): Una instancia de la clase `Servidor`.
            model (ConfigModel): Una instancia de la clase `ConfigModel`.
        """
        # Agregar el path al sys.path
        path = os.getcwd()
        module_path = os.path.join(path, "Servidor")
        ##module_path = '/home/al/Escritorio/TFG/Servidor/Modelo'
        if module_path not in sys.path:
            sys.path.append(module_path)

        # Importar el módulo usando la ruta absoluta
        from serverMain import Servidor
        
        self.serverModel = Servidor()
        self.model = ConfigModel()

    # Getter para el idioma
    def get_language(self):
        """
        Obtener la configuración actual del idioma.

        Returns:
            str: El idioma actual.
        """
        return self.model.language

    def set_language(self, language):
        """
        Establecer un nuevo idioma.

        Args:
            language (str): El nuevo idioma a establecer.
        """
        self.model.language = language

    def get_stt(self):
        """
        Obtener la configuración actual del servicio de reconocimiento de voz (STT).

        Returns:
            str: La configuración actual de STT.
        """
        return self.model.stt

    def set_stt(self, stt):
        """
        Establecer una nueva configuración para el servicio de reconocimiento de voz (STT).

        Args:
            stt (str): La nueva configuración de STT a establecer.

        Returns:
            ConfigModel: El modelo de configuración actualizado.
        """
        self.model.stt = stt
        return self.model

    def get_whisper_size(self):
        """
        Obtener la configuración actual del tamaño del modelo Whisper.

        Returns:
            str: El tamaño actual del modelo Whisper.
        """
        return self.model.whisper_size

    def set_whisper_size(self, whisper_size):
        """
        Establecer un nuevo tamaño para el modelo Whisper.

        Args:
            whisper_size (str): El nuevo tamaño del modelo Whisper a establecer.

        Returns:
            ConfigModel: El modelo de configuración actualizado.
        """
        self.model.whisper_size = whisper_size
        return self.model

    def get_llm(self):
        """
        Obtener la configuración actual del modelo de lenguaje grande (LLM).

        Returns:
            str: La configuración actual de LLM.
        """
        return self.model.llm

    def set_llm(self, llm):
        """
        Establecer una nueva configuración para el modelo de lenguaje grande (LLM).

        Args:
            llm (str): La nueva configuración de LLM a establecer.

        Returns:
            ConfigModel: El modelo de configuración actualizado.
        """
        self.model.llm = llm
        return self.model

    def get_llm_models(self):
        """
        Obtener la configuración actual de los modelos LLM.

        Returns:
            str: Los modelos LLM actuales.
        """
        return self.model.llm_models

    def set_llm_models(self, llm_models):
        """
        Establecer nuevos modelos LLM.

        Args:
            llm_models (str): Los nuevos modelos LLM a establecer.

        Returns:
            ConfigModel: El modelo de configuración actualizado.
        """   
        self.model.llm_models = llm_models
        return self.model

    def get_tts(self):
        """
        Obtener la configuración actual del servicio de texto a voz (TTS).

        Returns:
            str: La configuración actual de TTS.
        """
        return self.model.tts

    def set_tts(self, tts):
        """
        Establecer una nueva configuración para el servicio de texto a voz (TTS).

        Args:
            tts (str): La nueva configuración de TTS a establecer.

        Returns:
            ConfigModel: El modelo de configuración actualizado.
        """
        self.model.tts = tts
        return self.model

    def get_port(self):
        """
        Obtener la configuración actual del puerto.

        Returns:
            int: El puerto actual.
        """
        return self.model.port

    def set_port(self, port):
        """
        Establecer un nuevo puerto.

        Args:
            port (int): El nuevo puerto a establecer.

        Returns:
            ConfigModel: El modelo de configuración actualizado.
        """
        self.model.port = port
        return self.model

    def launch_server(self): 
        """
        Lanza el servidor con las configuraciones actuales.
        """
        port = self.model.port
        intport = int(port)
        self.serverModel.run(language=self.model.language, stt=self.model.stt, whisperSize=self.model.whisper_size, llm=self.model.llm, localModels=self.model.llm_models, tts=self.model.tts, port=intport)


if __name__ == "__main__":
    # Importar el servidor
    controller = ConfigController()
