from Modelo.serverMain import Servidor


class ServerController: 

    def __init__(self):
        self.model = Servidor()



    def launch_server(self, language, stt, whisperSize, llm, localModels, tts,port): 
        """
        print("Language:", language)
        print("STT:", stt)
        print("WhisperSize:", whisperSize)
        print("LLM:", llm)
        print("TTS:", tts)
        
        print("Local Models:", localModels)
        print("Port:", port)
        """
        self.model.serverHelloWorld()
        self.model.run(language=language, stt=stt, whisperSize=whisperSize, llm=llm, localModels=localModels, tts=tts, port=port)
         

if __name__ == "__main__":
    controller = ServerController()
