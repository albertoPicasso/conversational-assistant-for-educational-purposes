from .teacherInterface import TeacherInterface


## Implementation of LlmInterface using OpenAI API

class LanguageTeacher(TeacherInterface):
    def __init__(self, lang) :
        self.lang = lang
         

    def checkEndChat(self, message: str) -> bool:
        """
        Checks if the message indicates the end of the chat based on certain levels.

        Args:
        - message (str): The message to be checked for indicating the end of the chat.

        Returns:
        - bool: True if the message contains any of the predefined levels, False otherwise.
        """
        levels = ["A1","A2","B1","B2","C1","C2", "[END]"]
        for level in levels: 
            if level in message:
                return True
        
        return False 
    
    
    def evaluation(self, message_list, last_message, LLM )-> str:
        chat =  []
        #Create the systemMessage
        keyString  = (
        "Evaluate the following transcribed conversation from a speaking test according to the "
        "Common European Framework of Reference (CEFR) language proficiency levels. Focus on the following aspects, "
        "which are assessable from a written transcript: "
        "1. Coherence: Assess how logically ideas are connected and if the conversation flows logically from one point to another. "
        "2. Range of Vocabulary: Evaluate the variety and appropriateness of the vocabulary used. "
        "3. Grammatical Accuracy: Determine the correctness of the grammar used throughout the conversation. "
        "Please provide an assessment considering these aspects and indicate the approximate CEFR level (A1, A2, B1, B2, C1, C2) "
        "And how to improve it"
        "Dont forget to indicate the approximate CEFR level"
        )
        if (self.lang == "es"): language = "Please answer in spanish"
        if (self.lang == "en"): language = "Please answer in english"
        if (self.lang == "de"): language = "Please answer in German"

        systemMessage = keyString + language
        
        #Create the new message list
        message_to_append = ["system", systemMessage]
        chat.append(message_to_append)

        #Append all the new messages except system message
        for message_to_append in message_list[1:]: 
            chat.append(message_to_append)

        #Ask to LLM (local if server is in local llm mode or remote if server is in remote llmmode)
        #It uses the same class that the server, so it have an identical set up and behaviour
        
        last_message = LLM.request_to_llm(chat, 0.3)

        return last_message