from STTFolder.localWhisper import LocalWhisper
from STTFolder.remoteWhisper import RemoteWhisper
from LLMFolder.openAIAPI import OpenAIAPI
from TTSFolder.coquiTTS import CoquiTTS
from TTSFolder.openAITTS import OpenAITTS
import os
from openai import OpenAI


class Servidor:
    def __init__(self):
        ## Server variables
        self.systemMessage = "asistente tan simpatico que da ascoque "#"You are an Spanish teacher doing a speaking test. You must to act like a teacher, dont say that you are chatgpt. Do questions one by one and wait to my anwser. You should do 3 questions. At the end you send me a message whith a score using MCER levels and finally why i have this level and how to improve it . Remember that you only have 3 questions so choose wisely, dont do silly questions.I need that you more accurate whit scores. Not everyone can be a B2. Look the tenses, the complexiti of the phrases. Please be more accurate Speak every time in spanish."
        self.chat = [["system",self.systemMessage]]

        ##Configs

        #Online services
        self.client = OpenAI(api_key=os.getenv("OPENAIKEY"), base_url="https://api.openai.com/v1")
        ##STT        
        #self.STT = RemoteWhisper("whisper-1", self.client)

        ##LLM
        self.model = "gpt-3.5-turbo-0125"
        self.LLM = OpenAIAPI(self.client, self.model)

        #TTS
        #self.TTS = OpenAITTS("onyx")


        ##Local services
        ##STT
        self.modelSize = "small"
        self.STT = LocalWhisper(self.modelSize)
        
        ##LLM
        #self.client = OpenAI(base_url="http://192.168.1.135:1234/v1", api_key="lm-studio") 
        #self.model = "local-model"

        #TTS
        self.TTS = CoquiTTS("tts_models/es/css10/vits")
         


    def launch(self,filename ):
        
        
        text = self.STT.transcribe(filename)

        self.addMessageToChat(text, "user")

        request_mesagges = self.addMessagesToPetition()
        response = self.LLM.request_to_llm(request_mesagges)
        self.addMessageToChat(response, "assistant" )
        os.system("clear")
        self.printAllChat()
        outname = self.TTS.speak(response)
        return outname


    # Add new messages to list called chat whit format [role,message]
    def addMessageToChat(self, message, role):
        """
        Args:
        - message (str): The message to be added to the conversation.
        - role (str): The role of the participant sending the message (e.g., 'user', 'assistant', etc.).
        - chat (list): The conversation history to which the message will be added.

        Returns:
        None
        """
        message_entry = [role, message]
        self.chat.append(message_entry)

    # Create messages array to make a request with format ["role": rolemessage , "content": contentmessage }]
    def addMessagesToPetition(self): 
        """
        Args:
        - chat (list): The conversation history to be converted into a JSON request.

        Returns:
        list: A list of dictionaries representing each message in the conversation.
        """
        messages = []
        for message in self.chat: 
            messages.append({"role": message[0], "content": message[1]})
        return messages


    def printAllChat(self): 
        """
        Args:
        - chat (list): The conversation history to be printed.

        Returns:
        None
        """
        for message in self.chat: 
            if message[0] != "system":
                print(message[0] + ": " + message[1])

    def sayHI(self): 
        print("Hi from server")


"""
if __name__ == "__main__":
    server = Servidor()
    server.launch()
"""