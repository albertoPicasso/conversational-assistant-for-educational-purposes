import sys
import os
#from ..Servidor.Modelo.serverMain import Servidor
from configModel import ConfigModel


class ConfigController: 

    def __init__(self):

        # Add the path to sys.path
        module_path = '/home/al/Escritorio/TFG/Servidor/Modelo'
        if module_path not in sys.path:
            sys.path.append(module_path)

        # Import the module using the absolute path
        from serverMain import Servidor
        
        self.serverModel = Servidor()
        self.model = ConfigModel()


     # Getter for language
    def get_language(self):
        return self.model.language

    # Setter for language
    def set_language(self, language):
        self.model.language = language

    # Getter for stt
    def get_stt(self):
        return self.model.stt

    # Setter for stt
    def set_stt(self, stt):
        self.model.stt = stt
        return self.model

    # Getter for whisper_size
    def get_whisper_size(self):
        return self.model.whisper_size

    # Setter for whisper_size
    def set_whisper_size(self, whisper_size):
        self.model.whisper_size = whisper_size
        return self.model

    # Getter for llm
    def get_llm(self):
        return self.model.llm

    # Setter for llm
    def set_llm(self, llm):
        self.model.llm = llm
        return self.model

    # Getter for llm models
    def get_llm_models(self):
        return self.model.llm_models

    # Setter for models
    def set_llm_models(self, llm_models):
        self.model.llm_models = llm_models
        return self.model

    # Getter for tts
    def get_tts(self):
        return self.model.tts

    # Setter for tts
    def set_tts(self, tts):
        self.model.tts = tts
        return self.model

    # Getter for port
    def get_port(self):
        return self.model.port

    # Setter for port
    def set_port(self, port):
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
       
        self.serverModel.run(language=self.model.language, stt= self.model.stt, whisperSize= self.model.whisper_size, llm=self.model.llm, localModels=self.model.llm_models, tts=self.model.tts, port=self.model.port)
         

if __name__ == "__main__":
    ##Import Server


    controller = ConfigController()
