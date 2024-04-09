
from STTFolder.localWhisper import LocalWhisper
from STTFolder.remoteWhisper import RemoteWhisper
from LLMFolder.openAIAPI import OpenAIAPI
from TTSFolder.coquiTTS import CoquiTTS
from TTSFolder.openAITTS import OpenAITTS

import os
from openai import OpenAI

class Aux_functions:

    
    ## Add new messages to session['mensajes'] whit format [role,message]
    def addMessageToChat(self, message:str, role:str , state):
        """
        Args:
        - message (str): The message to be added to the conversation.
        - role (str): The role of the participant sending the message (e.g., 'user', 'assistant', etc.).
        - chat (list): The conversation history to which the message will be added.
        - state (session): The state of this client on server
        Returns: modified state
        """
        message_entry = [role, message]
        state['mensajes'].append(message_entry)
        return state


    def printAllChat(self, state): 
        """
        Args:
        - state (session): Contains the conversation history to be printed.

        Returns:
        None
        """
        message_list = state['mensajes']
        print('Lista de mensajes ')
        for message in message_list:
            print(message)

    
    def createUserDirectory(self, name:str):
        """
        Creates a new directory/folder with the specified name.

        Args:
        - name (str): The name of the directory to be created.

        Returns:
        None
        """
        #Path to new directory / folder
        path_to_directory = os.path.join(os.getcwd(), name)
        os.mkdir(path_to_directory)

    def createSTT(stt:str, whisperSize:str):

        if (stt == "local"): 
            stt = LocalWhisper(whisperSize)
            return stt
        elif (stt == "remoto"): 
            client = OpenAI(api_key=os.getenv("OPENAIKEY"), base_url="https://api.openai.com/v1")
            stt = RemoteWhisper("whisper-1", client)
            print ("Remote")
            return stt
        else: 
            raise TypeError("Error creating stt")
        

    def createLLM(llm:str):

        if (llm == "local"): 
            client = OpenAI(base_url="http://192.168.1.135:1234/v1", api_key="lm-studio") 
            model = "local-model"
            llm = OpenAIAPI(client, model)
            return llm
        elif (llm == "remoto"): 
            client = OpenAI(api_key=os.getenv("OPENAIKEY"), base_url="https://api.openai.com/v1")
            model = "gpt-3.5-turbo-0125"
            llm = OpenAIAPI(client, model)
            print("Remoto")
            return llm
        else: 
            print("Error")
            raise TypeError("Error creating LLM")
        
        
    def createTTS(tts:str, lang: str):
        
        if (tts == "remoto"): 
            tts = OpenAITTS("onyx")
            return tts
        elif (tts == "local" and lang == "es"): 
            tts = CoquiTTS("tts_models/es/css10/vits")
            return tts 
        elif (tts == "local" and lang == "en"): 
            tts = CoquiTTS("tts_models/en/ljspeech/fast_pitch")
            return tts
        elif (tts == "local" and lang == "de"): 
            tts = CoquiTTS("tts_models/de/css10/vits-neon")
            return tts
        else: 
            raise TypeError("Error creating TTS")
        
    def selectSysMessage(lang:str):
        if (lang == "es"):
            esMessage = "You are an Spanish teacher doing a speaking test. You must to act like a teacher, dont say that you are chatgpt. Do questions one by one and wait to my anwser. You should do 3 questions. At the end you send me a message whith a score using MCER levels and finally why i have this level and how to improve it . Remember that you only have 3 questions so choose wisely, dont do silly questions.I need that you more accurate whit scores. Look the tenses, the complexity of the phrases. Please be more accurate. Speak every time in spanish."
            return esMessage 
        elif (lang == "de"): 
            deMessage = "You are an German teacher doing a speaking test. You must to act like a teacher, dont say that you are chatgpt. Do questions one by one and wait to my anwser. You should do 3 questions. At the end you send me a message whith a score using MCER levels and finally why i have this level and how to improve it . Remember that you only have 3 questions so choose wisely, dont do silly questions.I need that you more accurate whit scores. Look the tenses, the complexity of the phrases. Please be more accurate. Speak every time in german."
            return deMessage
        elif (lang == "en"):
            enMessage ="You are an English teacher doing a speaking test. You must to act like a teacher, dont say that you are chatgpt. Do questions one by one and wait to my anwser. You should do 3 questions. At the end you send me a message whith a score using MCER levels and finally why i have this level and how to improve it . Remember that you only have 3 questions so choose wisely, dont do silly questions.I need that you more accurate whit scores. Look the tenses, the complexity of the phrases. Please be more accurate. Speak every time in English."
            return enMessage
        else: 
            raise TypeError("Not valid language")
        
    def replace_number(text : str, lang ): 

        if(lang == "es"): 
            new_text = text.replace("B2", "be dos" )
            new_text = new_text.replace("B1", "be uno")
            new_text = new_text.replace("A1", "a uno")
            new_text = new_text.replace("A2", "a dos")
            new_text = new_text.replace("C1", "ce uno")
            new_text = new_text.replace("C2", "ce uno")
            return new_text
        
        elif(lang == "en"): 
            new_text = text.replace("B2", "bee two")
            new_text = new_text.replace("B1", "bee one")
            new_text = new_text.replace("A1", "ay one")
            new_text = new_text.replace("A2", "ay two")
            new_text = new_text.replace("C1", "see one")
            new_text = new_text.replace("C2", "see two")
            return new_text
            
        elif(lang == "de"): 
            new_text = text.replace("B2", "bee zwei")
            new_text = new_text.replace("B1", "bee eins")
            new_text = new_text.replace("A1", "ah eins")
            new_text = new_text.replace("A2", "ah zwei")
            new_text = new_text.replace("C1", "tseh eins")
            new_text = new_text.replace("C2", "tseh zwei")
            return new_text