
from STTFolder.localWhisper import LocalWhisper
from STTFolder.remoteWhisper import RemoteWhisper
from LLMFolder.openAIAPI import OpenAIAPI
from TTSFolder.coquiTTS import CoquiTTS
from TTSFolder.openAITTS import OpenAITTS
from TeacherFolder.languageTeacher import LanguageTeacher

import os
from openai import OpenAI

import sqlite3
import bcrypt

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


    def printAllChat(state): 
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
        path_to_directory = os.path.join(os.getcwd(), "tempUserData",name)
        os.mkdir(path_to_directory)

    def createSTT(stt:str, whisperSize:str):
        """
        Creates an instance of a speech-to-text (STT) system, specified to be either local or remote. The type of STT
        system is determined by the 'stt' parameter, and its configuration is influenced by the 'whisperSize' or the API settings.

        Args:
        - stt (str): Specifies the type of STT system to create. Options are "local" for a locally run Whisper model or "remoto" for a remote service.
        - whisperSize (str): Configuration size for the Whisper model if 'stt' is "local".

        Returns:
        - object: An instance of either LocalWhisper or RemoteWhisper based on the 'stt' parameter.

        Raises:
        - TypeError: If the 'stt' parameter is not one of the recognized options.
        """

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
        """
        Creates an instance of a speech-to-text (STT) system, either local or remote, based on the specified type.

        Args:
        - stt (str): The type of STT system to create, "local" for a local system or "remoto" for a remote system.
        - whisperSize (str): The configuration size for the Whisper model if a local STT system is chosen.
        Returns:
        - object: An instance of LocalWhisper or RemoteWhisper based on the specified type.

        Raises:
        - TypeError: If an unrecognized STT system type is specified.
        """

        if (llm == "local"): 
            client = OpenAI(base_url="http://192.168.0.14:1234/v1", api_key="lm-studio") 
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
        """
        Creates an instance of a text-to-speech (TTS) system, configured according to the specified type and language.

        Args:
        - tts (str): The type of TTS system to create. Options are "remoto" for a remote system or "local" for a local system.
        - lang (str): The language for the TTS system. Valid options are "es" for Spanish, "en" for English, or "de" for German.

        Returns:
        - object: An instance of either OpenAITTS or CoquiTTS based on the specified type and language.

        Raises:
        - TypeError: If an unrecognized TTS system type or language is specified.
        """

        ##If error change max_len = 5000 in 
        #gedit /home/al/Escritorio/TFG_env/lib/python3.10/site-packages/TTS/tts/layers/generic/pos_encoding.py
        ##Delete models in 
        # /home/al/.local/share/tts/tts_models--en--multi-dataset--tortoise-v2

        if (tts == "remoto"): 
            tts = OpenAITTS("onyx")
            return tts
        elif (tts == "local" and lang == "es"): 
            tts = CoquiTTS("tts_models/es/css10/vits")
            return tts 
        elif (tts == "local" and lang == "en"): 
            tts = CoquiTTS("tts_models/en/ljspeech/vits")
            #tts = CoquiTTS("tts_models/en/multi-dataset/tortoise-v2")
            return tts
        elif (tts == "local" and lang == "de"): 
            tts = CoquiTTS("tts_models/de/css10/vits-neon")
            return tts
        else: 
            raise TypeError("Error creating TTS")
        

    def createLenguageTeacher(lang: str):
        """
        Creates and returns a LanguageTeacher instance for the specified language.

        This function initializes a LanguageTeacher object using the provided language code.

        Args:
        - lang (str): The language code for the language teacher. 

        Returns:
        - LanguageTeacher: An instance of the LanguageTeacher class initialized with the specified language.

        Raises:
        - TypeError: If the provided 'lang' is not a valid language code.
        """
        tm = LanguageTeacher(lang)
        return tm
        
    def selectSysMessage(lang:str):
        """
        Selects and returns a system message tailored for a language-specific speaking test simulation. The message instructs
        the user on how to conduct the test as if they were a language teacher, specifying the approach to questioning, the 
        scoring method, and the expectation for detailed feedback.

        Args:
        - lang (str): The language of the speaking test. Valid options are "es" for Spanish, "de" for German, and "en" for English.

        Returns:
        - str: A detailed message containing instructions for conducting a speaking test in the specified language.

        Raises:
        - TypeError: If the provided 'lang' is not one of the recognized options.
        """

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
        """
        Replaces specific alphanumeric symbols in a given text with their pronunciation equivalents in the specified language.
        This version is configured for Spanish ('es'), English ('en') and German ('de'), replacing sequences like 'B2' with 'be dos' according to how they
        are pronounced in the language.

        Args:
        - text (str): The original text containing alphanumeric symbols that need to be replaced.
        - lang (str): The language code that determines how replacements should be conducted. Currently only 'es' (Spanish) is implemented.

        Returns:
        - str: The modified text with symbols replaced by their pronunciation in the specified language.

        Raises:
        - ValueError: If the 'lang' is not supported or implemented.
        """

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
    
    
    def create_conexion(db_file):
        """
        Creates and returns a connection to the specified SQLite database file. 

        This function attempts to establish a connection to the SQLite database specified by 'db_file'. 
        If the connection fails, it catches the sqlite3.Error exception and prints an error message.

        Args:
        - db_file (str): The path to the SQLite database file.

        Returns:
        - sqlite3.Connection or None: A connection object to the SQLite database, or None if the connection fails.

        Raises:
        - sqlite3.Error: If an error occurs while trying to connect to the database.
        """

        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            raise TypeError(f"Error al conectar a la base de datos: {e}")
        return conn
    
    def create_table(conn):
        """
        Creates a 'usuarios' table in the specified SQLite database if it does not already exist.

        This function uses the provided database connection to create a table named 'usuarios' with 
        the following columns:
        - id: An integer primary key that auto-increments.
        - nombre: A text field that cannot be null.
        - usuario: A unique text field that cannot be null.
        - contrasena: A text field that cannot be null.

        Args:
        - conn (sqlite3.Connection): The connection object to the SQLite database.

        Returns:
        - None
        """

        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            usuario TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL
        )
        ''')
        

    def add_user( nombre, usuario, contrasena):
        """
        Adds a new user to the 'usuarios' table in the 'users.db' SQLite database.

        This function connects to the 'users.db' SQLite database and inserts a new record into the 'usuarios' table.
        The password is hashed using bcrypt before storing it in the database.

        Args:
        - nombre (str): The name of the user.
        - usuario (str): The unique username of the user.
        - contrasena (str): The plaintext password of the user.

        Returns:
        - None

        Raises:
        - sqlite3.Error: If an error occurs while interacting with the SQLite database.
        - bcrypt.Error: If an error occurs while hashing the password.
        """

        conn = sqlite3.connect('users.db')
        salt = bcrypt.gensalt()
        pass_hashed = bcrypt.hashpw(contrasena.encode('utf-8'), salt)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (nombre, usuario, contrasena) VALUES (?, ?, ?)', (nombre, usuario, pass_hashed))
        conn.commit()
        

    def verify_user(username, password):
        """
        Verifies a user's credentials against the 'usuarios' table in the 'users.db' SQLite database.

        This function connects to the 'users.db' SQLite database and retrieves the hashed password for the 
        specified username. It then checks if the provided plaintext password matches the hashed password 
        stored in the database using bcrypt.

        Args:
        - username (str): The username of the user to verify.
        - password (str): The plaintext password of the user to verify.

        Returns:
        - bool: True if the credentials are valid, False otherwise.

        Raises:
        - sqlite3.Error: If an error occurs while interacting with the SQLite database.
        - bcrypt.Error: If an error occurs while checking the hashed password.
        """

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT contrasena FROM usuarios WHERE usuario = ?', (username,))
        result = cursor.fetchone()

        if result is None:
            return False

        pass_hashed = result[0]

        if bcrypt.checkpw(password.encode('utf-8'), pass_hashed):
            return True
        else:
            return False

        



    