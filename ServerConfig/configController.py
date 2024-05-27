import sys
import os
# ..from Servidor.Modelo.serverMain import Servidor
from configModel import ConfigModel


class ConfigController: 
    """
    Controller class for managing server configuration settings.

    This class handles the logic for managing and updating server configuration settings such as 
    language, speech-to-text (STT) service, large language model (LLM), text-to-speech (TTS) service, 
    Whisper model size, and server port. It interfaces with the model to retrieve and set these settings.
    """
    def __init__(self):
        """
        Initialize the main application.

        This constructor performs the following actions:
        - Adds the current working directory to the system path.
        - Adds the specific module path to the system path if it's not already present.
        - Imports the `Servidor` class from the `serverMain` module.
        - Initializes an instance of the `Servidor` class and assigns it to `self.serverModel`.
        - Initializes an instance of the `ConfigModel` class and assigns it to `self.model`.

        Attributes:
            serverModel (Servidor): An instance of the `Servidor` class.
            model (ConfigModel): An instance of the `ConfigModel` class.
        """
        # Add the path to sys.path
        path = os.getcwd()
        module_path = os.path.join (path, "Servidor")
        ##module_path = '/home/al/Escritorio/TFG/Servidor/Modelo'
        if module_path not in sys.path:
            sys.path.append(module_path)

        # Import the module using the absolute path
        from serverMain import Servidor
        
        self.serverModel = Servidor()
        self.model = ConfigModel()




     # Getter for language
    def get_language(self):
        """
        Get the current language setting.

        Returns:
            str: The current language.
        """
        return self.model.language

    def set_language(self, language):
        """
        Set a new language.

        Args:
            language (str): The new language to set.
        """
        self.model.language = language

    def get_stt(self):
        """
        Get the current speech-to-text (STT) setting.

        Returns:
            str: The current STT setting.
        """
        return self.model.stt

    def set_stt(self, stt):
        """
        Set a new speech-to-text (STT) setting.

        Args:
            stt (str): The new STT setting to set.

        Returns:
            ConfigModel: The updated configuration model.
        """
        self.model.stt = stt
        return self.model

    def get_whisper_size(self):
        """
        Get the current Whisper model size setting.

        Returns:
            str: The current Whisper model size.
        """
        return self.model.whisper_size

    def set_whisper_size(self, whisper_size):
        """
        Set a new Whisper model size.

        Args:
            whisper_size (str): The new Whisper model size to set.

        Returns:
            ConfigModel: The updated configuration model.
        """
        self.model.whisper_size = whisper_size
        return self.model

    def get_llm(self):
        """
        Get the current large language model (LLM) setting.

        Returns:
            str: The current LLM setting.
        """
        return self.model.llm

    def set_llm(self, llm):
        """
        Set a new large language model (LLM) setting.

        Args:
            llm (str): The new LLM setting to set.

        Returns:
            ConfigModel: The updated configuration model.
        """
        self.model.llm = llm
        return self.model

    def get_llm_models(self):
        """
        Get the current LLM models setting.

        Returns:
            str: The current LLM models.
        """
        return self.model.llm_models

    def set_llm_models(self, llm_models):
        """
        Set new LLM models.

        Args:
            llm_models (str): The new LLM models to set.

        Returns:
            ConfigModel: The updated configuration model.
        """   
        self.model.llm_models = llm_models
        return self.model

    def get_tts(self):
        """
        Get the current text-to-speech (TTS) setting.

        Returns:
            str: The current TTS setting.
        """
        return self.model.tts

    def set_tts(self, tts):
        """
        Set a new text-to-speech (TTS) setting.

        Args:
            tts (str): The new TTS setting to set.

        Returns:
            ConfigModel: The updated configuration model.
        """
        self.model.tts = tts
        return self.model

    def get_port(self):
        """
        Get the current port setting.

        Returns:
            int: The current port.
        """
        return self.model.port

    def set_port(self, port):
        """
        Set a new port.

        Args:
            port (int): The new port to set.

        Returns:
            ConfigModel: The updated configuration model.
        """
        self.model.port = port
        return self.model


    def launch_server(self): 
        """
        print("Language:", language)
        print("STT:", stt)
        print("WhisperSize:", whisperSize)
        print("LLM:", llm)
        print("TTS:", tts)
        
        print("Local Models:", localModels)
        print("Port:", port)
        """
        port = self.model.port
        intport = int (port)
        self.serverModel.run(language=self.model.language, stt= self.model.stt, whisperSize= self.model.whisper_size, llm=self.model.llm, localModels=self.model.llm_models, tts=self.model.tts, port=intport)
         

if __name__ == "__main__":
    ##Import Server
    controller = ConfigController()
