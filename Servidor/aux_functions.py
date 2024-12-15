
from STTs.localWhisper import LocalWhisper
from STTs.remoteWhisper import RemoteWhisper
from LLMs.openAIAPI import OpenAIAPI
from TTSs.coquiTTS import CoquiTTS
from TTSs.openAITTS import OpenAITTS
from Teachersubject.languageTeacher import LanguageTeacher

import os
from openai import OpenAI
from pydub import AudioSegment
from pydub.silence import detect_nonsilent


import sqlite3
import bcrypt

class Aux_functions:

    
    ## Add new messages to session['mensajes'] whit format [role,message]
    def addMessageToChat(self, message:str, role:str , state):
        """
        Añade un mensaje a la conversación.

        Args:
            message (str): El mensaje a añadir a la conversación.
            role (str): El rol del participante que envía el mensaje (por ejemplo, 'user', 'assistant', etc.).
            state (session): El estado de este cliente en el servidor.

        Returns:
            dict: El estado modificado.
        """
        message_entry = [role, message]
        state['mensajes'].append(message_entry)
        return state


    def printAllChat(state): 
        """
        Imprime todo el historial de la conversación.

        Args:
            state (session): Contiene el historial de la conversación a imprimir.

        Returns:
            None
        """
        message_list = state['mensajes']
        print('Lista de mensajes ')
        for message in message_list:
            print(message)

    
    def createUserDirectory(self, name:str):
        """
        Crea un nuevo directorio/carpeta con el nombre especificado.

        Args:
            name (str): El nombre del directorio a crear.

        Returns:
            None
        """
        #Path to new directory / folder
        path_to_directory = os.path.join(os.getcwd(), "tempUserData",name)
        os.mkdir(path_to_directory)

    def createSTT(stt:str, whisperSize:str):
        """
        Crea una instancia de un sistema de reconocimiento de voz a texto (STT), que puede ser local o remoto. El tipo de sistema STT
        se determina por el parámetro 'stt', y su configuración se influye por el 'whisperSize' o la configuración de la API.

        Args:
            stt (str): Especifica el tipo de sistema STT a crear. Las opciones son "local" para un modelo Whisper ejecutado localmente o "remoto" para un servicio remoto.
            whisperSize (str): Tamaño de configuración para el modelo Whisper si 'stt' es "local".

        Returns:
            object: Una instancia de LocalWhisper o RemoteWhisper basada en el parámetro 'stt'.

        Raises:
            TypeError: Si el parámetro 'stt' no es una de las opciones reconocidas.
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
        Crea una instancia de un sistema de reconocimiento de voz a texto (STT), ya sea local o remoto, según el tipo especificado.

        Args:
            stt (str): El tipo de sistema STT a crear, "local" para un sistema local o "remoto" para un sistema remoto.
            whisperSize (str): El tamaño de configuración para el modelo Whisper si se elige un sistema STT local.

        Returns:
            object: Una instancia de LocalWhisper o RemoteWhisper según el tipo especificado.

        Raises:
            TypeError: Si se especifica un tipo de sistema STT no reconocido.
        """

        if (llm == "local"): 
            client = OpenAI(base_url="http://192.168.0.14:1234/v1", api_key="lm-studio") 
            model = "local-model"
            llm = OpenAIAPI(client, model)
            return llm
        elif (llm == "remoto"): 
            client = OpenAI(api_key=os.getenv("OPENAIKEY"), base_url="https://api.openai.com/v1")
            model ="gpt-4o"#"gpt-3.5-turbo-0125"#
            llm = OpenAIAPI(client, model)
            print("Remoto")
            return llm
        else: 
            print("Error")
            raise TypeError("Error creating LLM")
        
        
    def createTTS(tts:str, lang: str):
        """
        Crea una instancia de un sistema de texto a voz (TTS), configurado según el tipo y el idioma especificados.

        Args:
            tts (str): El tipo de sistema TTS a crear. Las opciones son "remoto" para un sistema remoto o "local" para un sistema local.
            lang (str): El idioma para el sistema TTS. Las opciones válidas son "es" para español, "en" para inglés o "de" para alemán.

        Returns:
            object: Una instancia de OpenAITTS o CoquiTTS según el tipo y el idioma especificados.

        Raises:
            TypeError: Si se especifica un tipo de sistema TTS o un idioma no reconocido.
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
        Crea y devuelve una instancia de LanguageTeacher para el idioma especificado.

        Esta función inicializa un objeto LanguageTeacher utilizando el código de idioma proporcionado.

        Args:
            lang (str): El código de idioma para el profesor de idiomas.

        Returns:
            LanguageTeacher: Una instancia de la clase LanguageTeacher inicializada con el idioma especificado.

        Raises:
            TypeError: Si el 'lang' proporcionado no es un código de idioma válido.
        """

        tm = LanguageTeacher(lang)
        return tm
        
    def selectSysMessage(lang:str):
        """
        Selecciona y devuelve un mensaje del sistema adaptado para una simulación de prueba de conversación específica del idioma.
        El mensaje instruye al usuario sobre cómo realizar la prueba como si fuera un profesor de idiomas, especificando el enfoque 
        para las preguntas, el método de calificación y la expectativa de retroalimentación detallada.

        Args:
            lang (str): El idioma de la prueba de conversación. Las opciones válidas son "es" para español, "de" para alemán y "en" para inglés.

        Returns:
            str: Un mensaje detallado que contiene instrucciones para realizar una prueba de conversación en el idioma especificado.

        Raises:
            TypeError: Si el 'lang' proporcionado no es una de las opciones reconocidas.
        """

        if (lang == "es"):
            esMessage = "You are a Spanish teacher conducting a speaking test. You must act like a teacher and not mention that you are ChatGPT. Ask questions one by one and wait for my answer. You should ask 3 questions. At the end, send me a message with a score using CEFR levels, explaining why I have this level and how to improve it. Remember, you only have 3 questions, so choose wisely and avoid trivial questions. Be accurate with the scores, evaluating the tenses and complexity of the phrases. Speak only in Spanish and do not use special characters."
            return esMessage 
        elif (lang == "de"): 
            deMessage = "You are a German teacher conducting a speaking test. You must act like a teacher and not mention that you are ChatGPT. Ask questions one by one and wait for my answer. You should ask 3 questions. At the end, send me a message with a score using CEFR levels, explaining why I have this level and how to improve it. Remember, you only have 3 questions, so choose wisely and avoid trivial questions. Be accurate with the scores, evaluating the tenses and complexity of the phrases. Speak only in German and do not use special characters. "
            return deMessage
        elif (lang == "en"):
            enMessage ="You are a English teacher conducting a speaking test. You must act like a teacher and not mention that you are ChatGPT. Ask questions one by one and wait for my answer. You should ask 3 questions. At the end, send me a message with a score using CEFR levels, explaining why I have this level and how to improve it. Remember, you only have 3 questions, so choose wisely and avoid trivial questions. Be accurate with the scores, evaluating the tenses and complexity of the phrases. Speak only in English and do not use special characters."
            return enMessage
        else: 
            raise TypeError("Not valid language")
        
    def replace_number(text : str, lang ): 
        """
        Reemplaza símbolos alfanuméricos específicos en un texto dado con sus equivalentes de pronunciación en el idioma especificado.
        Esta versión está configurada para español ('es'), inglés ('en') y alemán ('de'), reemplazando secuencias como 'B2' con 'be dos' 
        según cómo se pronuncian en el idioma.

        Args:
            text (str): El texto original que contiene los símbolos alfanuméricos que deben ser reemplazados.
            lang (str): El código de idioma que determina cómo se deben realizar los reemplazos. Actualmente solo se implementa 'es' (español).

        Returns:
            str: El texto modificado con los símbolos reemplazados por su pronunciación en el idioma especificado.

        Raises:
            ValueError: Si el 'lang' no es compatible o no está implementado.
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
    
    
    def remove_silence(input_file, silence_thresh=-50, min_silence_len=500, padding=300):
        """
        Transcribe un archivo de audio usando el modelo Whisper y elimina silencios absolutos.

        Args:
            filename (str): La ruta del archivo de audio a transcribir.
            logprob_threshold (float): Si la probabilidad logarítmica promedio sobre los tokens muestreados es inferior a este valor, se considera fallido. Valores más bajos hacen que el modelo sea más permisivo.
            no_speech_threshold (float): Si la probabilidad de no-habla es mayor que este valor Y la probabilidad logarítmica promedio sobre los tokens muestreados es inferior a logprob_threshold, se considera el segmento como silencioso. Valores más bajos hacen que el modelo sea más estricto en la identificación de silencios.

        Returns:
            dict: Un diccionario que contiene los resultados de la transcripción.

        Raises:
            FileNotFoundError: Si el archivo especificado no se encuentra.
            ValueError: Si los parámetros logprob_threshold o no_speech_threshold son inválidos.
        """

        # Cargar el archivo de audio
        audio = AudioSegment.from_file(input_file)
        
        # Detectar segmentos no silenciosos
        non_silent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
        
        # Recortar y combinar segmentos no silenciosos
        chunks = [audio[start-padding:end+padding] for start, end in non_silent_ranges]
        output_audio = AudioSegment.empty()
        for chunk in chunks:
            output_audio += chunk
        
        # Exportar el archivo de audio resultante
        os.remove(input_file)
        output_audio.export(input_file, format="wav")
        


    def create_conexion(db_file):
        """
        Crea y devuelve una conexión al archivo de base de datos SQLite especificado.

        Esta función intenta establecer una conexión con la base de datos SQLite especificada por 'db_file'. 
        Si la conexión falla, captura la excepción sqlite3.Error e imprime un mensaje de error.

        Args:
            db_file (str): La ruta al archivo de base de datos SQLite.

        Returns:
            sqlite3.Connection or None: Un objeto de conexión a la base de datos SQLite, o None si la conexión falla.

        Raises:
            sqlite3.Error: Si ocurre un error al intentar conectar a la base de datos.
        """

        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            raise TypeError(f"Error al conectar a la base de datos: {e}")
        return conn
    
    def create_table(conn):
        """
        Crea una tabla 'usuarios' en la base de datos SQLite especificada si no existe.

        Esta función utiliza la conexión de base de datos proporcionada para crear una tabla llamada 'usuarios' con 
        las siguientes columnas:
            - id: Una clave primaria entera que se auto incrementa.
            - nombre: Un campo de texto que no puede ser nulo.
            - usuario: Un campo de texto único que no puede ser nulo.
            - contrasena: Un campo de texto que no puede ser nulo.

        Args:
            conn (sqlite3.Connection): El objeto de conexión a la base de datos SQLite.

        Returns:
            None
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
        Añade un nuevo usuario a la tabla 'usuarios' en la base de datos SQLite 'users.db'.

        Esta función se conecta a la base de datos SQLite 'users.db' e inserta un nuevo registro en la tabla 'usuarios'.
        La contraseña se cifra utilizando bcrypt antes de almacenarla en la base de datos.

        Args:
            nombre (str): El nombre del usuario.
            usuario (str): El nombre de usuario único del usuario.
            contrasena (str): La contraseña en texto plano del usuario.

        Returns:
            None

        Raises:
            sqlite3.Error: Si ocurre un error al interactuar con la base de datos SQLite.
            bcrypt.Error: Si ocurre un error al cifrar la contraseña.
        """

        conn = sqlite3.connect('users.db')
        salt = bcrypt.gensalt()
        pass_hashed = bcrypt.hashpw(contrasena.encode('utf-8'), salt)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (nombre, usuario, contrasena) VALUES (?, ?, ?)', (nombre, usuario, pass_hashed))
        conn.commit()
        

    def verify_user(username, password):
        """
        Verifica las credenciales de un usuario contra la tabla 'usuarios' en la base de datos SQLite 'users.db'.

        Esta función se conecta a la base de datos SQLite 'users.db' y recupera la contraseña cifrada para el 
        nombre de usuario especificado. Luego verifica si la contraseña en texto plano proporcionada coincide 
        con la contraseña cifrada almacenada en la base de datos utilizando bcrypt.

        Args:
            username (str): El nombre de usuario del usuario a verificar.
            password (str): La contraseña en texto plano del usuario a verificar.

        Returns:
            bool: True si las credenciales son válidas, False en caso contrario.

        Raises:
            sqlite3.Error: Si ocurre un error al interactuar con la base de datos SQLite.
            bcrypt.Error: Si ocurre un error al verificar la contraseña cifrada.
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

    
    def delete_user(username, password):
        """
        Elimina un usuario de la tabla 'usuarios' en la base de datos SQLite 'users.db' si las credenciales proporcionadas son válidas.

        Esta función se conecta a la base de datos SQLite 'users.db' y recupera la contraseña cifrada para el 
        nombre de usuario especificado. Luego verifica si la contraseña en texto plano proporcionada coincide 
        con la contraseña cifrada almacenada en la base de datos utilizando bcrypt. Si las credenciales son válidas, 
        elimina al usuario de la base de datos.

        Args:
            username (str): El nombre de usuario del usuario a eliminar.
            password (str): La contraseña en texto plano del usuario a verificar.

        Returns:
            bool: True si el usuario fue eliminado, False en caso contrario.

        Raises:
            sqlite3.Error: Si ocurre un error al interactuar con la base de datos SQLite.
            bcrypt.Error: Si ocurre un error al verificar la contraseña cifrada.
        """

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # Verify the user's credentials
        cursor.execute('SELECT contrasena FROM usuarios WHERE usuario = ?', (username,))
        result = cursor.fetchone()

        if result is None:
            return False

        pass_hashed = result[0]

        if bcrypt.checkpw(password.encode('utf-8'), pass_hashed):
            # Credentials are valid, delete the user
            cursor.execute('DELETE FROM usuarios WHERE usuario = ?', (username,))
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False
        


    