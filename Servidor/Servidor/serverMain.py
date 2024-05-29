from flask import Flask, session, request, send_file, jsonify
import uuid
import os
from openai import OpenAI
import logging
import base64
import sys
import sqlite3

from aux_functions import Aux_functions


class Servidor:

    def __init__(self):

        """
        Inicializa la configuración del servidor y configura las rutas y la base de datos.

        Este constructor realiza las siguientes acciones:
        - Inicializa una aplicación Flask.
        - Establece una clave secreta para la aplicación Flask.
        - Inicializa funciones auxiliares.
        - Agrega reglas de URL para varios endpoints.
        - Crea una carpeta para datos temporales de usuarios si no existe.
        - Crea una base de datos para datos de usuarios si no existe y agrega un usuario predeterminado.

        Atributos:
            app (Flask): La instancia de la aplicación Flask.
            aux (Aux_functions): Una instancia de funciones auxiliares para varias operaciones de utilidad.

        Raises:
            sqlite3.Error: Si hay un error al agregar el usuario predeterminado a la base de datos.
        """
        
        ##Server configs
        self.app = Flask(__name__)
        self.app.secret_key = 'tu_clave_secreta'
        self.aux = Aux_functions()

        ## Adding rules
        self.app.add_url_rule('/', 'register_user_session', self.register_user_session, methods=['GET'])
        self.app.add_url_rule('/upload_wav', 'upload_wav', self.upload_wav, methods=['POST'])
        self.app.add_url_rule('/ping', 'ping', self.ping, methods=['GET'])
        self.app.add_url_rule('/logout', 'logout', self.logout, methods=['GET'])
        self.app.add_url_rule('/logIn', 'login', self.logIn, methods=['POST'])
        self.app.add_url_rule('/register_new_user', 'register_new_user', self.register_new_user, methods=['POST'])
        self.app.add_url_rule('/delete_user', 'delete_user', self.delete_user, methods=['POST'])

        folder_path = "tempUserData"
        ##Create data container
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        ##Create database if not exist
        conn = Aux_functions.create_conexion('users.db')
        if conn:
            Aux_functions.create_table(conn)
            conn.close()
        try:
            Aux_functions.add_user('Alberto M', 'al', 'al')
        except sqlite3.Error as e:
            print(f"Error al añadir usuario: {e}")
      
    
    def run(self, language = "es", stt = "local", whisperSize = "small" , llm = "remoto", localModels = "Gemma", tts = "local", port = 5000):
        """
        Ejecuta el servidor Flask con las configuraciones especificadas.

        Este método configura el registro, inicializa varios componentes del sistema (como STT, LLM y TTS)
        y arranca el servidor Flask.

        Args:
            language (str, optional): La configuración de idioma para el sistema. Por defecto es "es".
            stt (str, optional): El servicio de reconocimiento de voz a texto a utilizar. Por defecto es "local".
            whisperSize (str, optional): El tamaño del modelo Whisper a utilizar para STT. Por defecto es "small".
            llm (str, optional): El modelo de lenguaje grande a utilizar. Por defecto es "remoto".
            localModels (str, optional): Los modelos locales a utilizar. Por defecto es "Gemma".
            tts (str, optional): El servicio de texto a voz a utilizar. Por defecto es "local".
            port (int, optional): El puerto en el que se ejecutará el servidor Flask. Por defecto es 5000.

        Raises:
            Exception: Si ocurre una excepción no manejada durante la inicialización de los componentes del sistema.
        """
        #Set logger
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(formatter)
        self.app.logger.addHandler(file_handler)
        self.app.logger.setLevel(logging.DEBUG)
        self.app.logger.critical(f'Server Start ')
        self.lang = language
        
        ##Interface Config
        try:
            self.systemMessage = Aux_functions.selectSysMessage(language)
            self.STT = Aux_functions.createSTT(stt, whisperSize)
            self.LLM = Aux_functions.createLLM(llm)
            self.TTS = Aux_functions.createTTS(tts,language)
            self.teacherMode = Aux_functions.createLenguageTeacher(self.lang)
            print("Server is ready")
        except Exception as e:
            self.app.logger.error('Unhandled exception occurred. Leaving...', exc_info=e)
            sys.exit(-1)
       
        self.app.run(debug=True,host='0.0.0.0', port=port,  use_reloader=False)


    def register_new_user(self):
        """
        Registra un nuevo usuario basado en los datos JSON recibidos en la solicitud.

        Este método extrae la información del usuario de una carga útil JSON, intenta agregar al usuario
        a la base de datos y maneja cualquier error potencial durante el proceso. También registra
        el éxito o fracaso del intento de registro.

        Returns:
            tuple: Una tupla que contiene un mensaje y un código de estado HTTP.
                - "ok", 200: Si el usuario se registra con éxito.
                - "User already exist", 409: Si se intenta registrar un usuario existente.
                - "Something gone wrong", 500: Si ocurre una excepción no manejada.
        """
        try:
            if request.is_json:
                
                data = request.get_json()
                ip_address = request.remote_addr
                name = data.get('name')
                username = data.get('username')
                password = data.get('password')
                try:
                    Aux_functions.add_user(name, username, password)
                except sqlite3.Error as e:
                    self.app.logger.info (f'- User attemped to register / ip {ip_address} ')
                    return "User already exist", 409
                
                
                self.app.logger.info (f'- User Register Succsessfully ip {ip_address} ')
                return "ok", 200
                

        except Exception as e:
            self.app.logger.error('Unhandled exception occurred', exc_info=e)
            return "Something gone wrong", 500


    def logIn(self):
        """
        Autentica a un usuario basado en los datos JSON recibidos en la solicitud.

        Este método extrae el nombre de usuario y la contraseña de una carga útil JSON, verifica las credenciales del usuario
        y maneja el proceso de inicio de sesión. También registra el éxito o fracaso del intento de inicio de sesión.

        Returns:
            tuple: Una tupla que contiene un mensaje y un código de estado HTTP.
                - "Verifing user: OK", 200: Si el usuario se autentica con éxito.
                - "Verifing user: NOT OK", 401: Si la autenticación falla.
                - "something failed", 500: Si el formato de la solicitud es incorrecto o ocurre una excepción no manejada.
        """
        try:
            if request.is_json:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')

                flag = Aux_functions.verify_user(username, password)
                ip_address = request.remote_addr

                if (flag):
                    self.app.logger.info (f'- User Logged Succsessfully ip {ip_address} ')
                    return "Verifing user: OK", 200
                else:
                    self.app.logger.info (f'- User attemped to log ip {ip_address} ')
                    return "Verifing user: NOT OK", 401     
                
            else : 
                self.app.logger.info (f'- Bad format ip {ip_address} ')
                return "something failed", 500
        except Exception as e:
            self.app.logger.error('Unhandled exception occurred', exc_info=e)
            return 'Error verifing user: {}'.format(str(e)), 500


    def register_user_session(self):
        """
        Registra una nueva sesión de usuario e inicializa el estado de la sesión.

        Este método asigna un ID de usuario único a la sesión si aún no lo tiene,
        inicializa el estado de la sesión y los mensajes, agrega un mensaje del sistema al chat,
        crea un directorio de usuario y registra el éxito o fracaso del registro.

        Returns:
            tuple: Una tupla que contiene un mensaje y un código de estado HTTP.
                - 'User {user_id} registered successfully.', 200: Si la sesión de usuario se registra con éxito.
                - 'Error registering user: {error_message}', 500: Si ocurre una excepción no manejada durante el registro.
        """
        try:
            # Give a user_id if user is not registered
            if 'user_id' not in session:
                session['user_id'] = str(uuid.uuid4())
            user_id = session['user_id']
            
            # Create a "estado" variable in session object
            if 'estado' not in session:
                session['estado'] = {}
            state = session['estado']

            # Create a "mensajes" array in estado
            if 'mensajes' not in state:
                state['mensajes'] = []

            # Add system message to user chat
            state = self.aux.addMessageToChat(self.systemMessage, "system", state)

            # Save state in session
            session['estado'] = state
            
            self.aux.createUserDirectory(user_id)

            ip_address = request.remote_addr

            self.app.logger.info (f'- User Register Succsessfully id {user_id} / ip {ip_address} ')
            return 'User {} registered successfully.'.format(user_id), 200

        except Exception as e:
            self.app.logger.error('Unhandled exception occurred', exc_info=e)
            return 'Error registering user: {}'.format(str(e)), 500

  
    def upload_wav(self):
        """
        Maneja la carga de un archivo WAV, transcribe su contenido, interactúa con el modelo de lenguaje
        y devuelve una respuesta sintetizada.

        Este método realiza las siguientes acciones:
        - Verifica si el usuario está autenticado.
        - Valida la presencia y selección de un archivo WAV en la solicitud.
        - Guarda el archivo WAV cargado en un directorio temporal.
        - Transcribe el archivo WAV a texto utilizando el sistema STT.
        - Agrega el texto transcrito al historial del chat.
        - Envía el historial del chat a un modelo de lenguaje y recibe una respuesta.
        - Verifica si la conversación ha terminado y prepara un mensaje de evaluación si es necesario.
        - Agrega la respuesta del asistente al historial del chat.
        - Convierte la respuesta a voz utilizando el sistema TTS.
        - Codifica la respuesta de audio en base64 y la devuelve junto con una bandera de fin de conversación.

        Returns:
            Response: Una respuesta JSON que contiene el audio codificado y la bandera de fin de conversación, o un mensaje de error y un código de estado.
        """
        try:
            # Check if user is authenticated
            if 'user_id' not in session:
                return 'User not registered', 401

            # Get user ID
            user_id = session['user_id']

            # Check if a WAV file is provided in the request
            if 'wav_file' not in request.files:
                return 'No file sent', 404

            # Get the sent WAV file
            wav = request.files['wav_file']

            # Check if a WAV file is selected
            if wav.filename == '':
                return 'No WAV selected.', 404

            # Save the received file in client folder in server
            filename = 'inputServ.wav'
            path = os.path.join(os.getcwd(), "tempUserData",user_id, filename)
            wav.save(path)

            # Get session state
            state = session.get('estado', {})

            #Remove Silences
            Aux_functions.remove_silence(path)

            # Transcribe the WAV file
            text = self.STT.transcribe(path)

            state = self.aux.addMessageToChat(text, "user", state)
            

            # Ask to language model
            messages_list = state['mensajes']
            response = self.LLM.request_to_llm(messages_list)
            
            #Check if isEnd, if its True , prepare the message to TTS
            #If is teacher or some 
            isEnd = self.teacherMode.checkEndChat(response)
            if (isEnd): 
                response = self.teacherMode.evaluation(messages_list, response, self.LLM)
                response = Aux_functions.replace_number(response, self.lang)
            
            #Add message
            state = self.aux.addMessageToChat(response, "assistant", state)
            # Update session state
            session['estado'] = state
            
            # TTS
            outname = self.TTS.speak(response, user_id)
            
            # Prepare the audio file
            with open(outname, 'rb') as audio_file:
                audio_data = audio_file.read()

                # Codifica los datos binarios del audio en base64
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')

            
            response_data = {
                'audio': audio_base64,
                'flag': isEnd
                }
            
            self.app.logger.info (f'Processed audio from - id {user_id} ')
            return jsonify(response_data)

        except Exception as e:
            self.app.logger.error('Unhandled exception occurred', exc_info=e)
            return f"An error occurred: {str(e)}", 500
      
    
    def logout(self):
        """
        Cierra la sesión del usuario eliminando el ID de usuario de la sesión y borrando el directorio de datos temporales del usuario.

        Este método realiza las siguientes acciones:
        - Verifica si el usuario está autenticado.
        - Elimina el ID de usuario de la sesión.
        - Borra el directorio de datos temporales del usuario.
        - Registra el cierre de sesión exitoso.

        Returns:
            tuple: Una tupla que contiene un mensaje y un código de estado HTTP.
                - 'Logout successfully.', 200: Si el usuario cierra sesión con éxito.
                - 'An error occurred: {error_message}', 500: Si ocurre una excepción no manejada durante el cierre de sesión.
        """
        try:
            if 'user_id' in session:
                user_id = session['user_id']
                session.pop('user_id')
                "tempUserData"
            # Remove client directory 
            path = os.path.join(os.getcwd(), "tempUserData",user_id)
            os.system(f'rm -rf {path}')
            self.app.logger.info (f'- Logout user Succsessfully - id {user_id} /  ')
            return 'Logout successfully.', 200
                
        except Exception as e:
            self.app.logger.error('Unhandled exception occurred', exc_info=e)
            return f"An error occurred: {str(e)}", 500



    def delete_user (self ): 
        """
        Elimina un usuario basado en los datos JSON recibidos en la solicitud.

        Este método extrae el nombre de usuario y la contraseña de una carga útil JSON, intenta eliminar al usuario
        de la base de datos y maneja cualquier error potencial durante el proceso. También registra el éxito
        o fracaso del intento de eliminación.

        Returns:
            tuple: Una tupla que contiene un mensaje y un código de estado HTTP.
                - "User deleted", 200: Si el usuario se elimina con éxito.
                - "User not found", 400: Si el usuario no se encuentra o la eliminación falla.
                - "An error occurred: {error_message}", 500: Si ocurre una excepción no manejada.
        """
        try:
            if request.is_json:
                
                data = request.get_json()
                ip_address = request.remote_addr
                username = data.get('username')
                password = data.get('password')
                flag = Aux_functions.delete_user(username, password)
                
                if (flag):
                    self.app.logger.info (f'- Acount deleted / ip {ip_address} ')
                    return "User deleted", 200
                    
                else: 
                    self.app.logger.info (f'- Attempt to delete a acount/ ip {ip_address} ')
                    return "User not found", 400

        except Exception as e:
            self.app.logger.error('Unhandled exception occurred', exc_info=e)
            return f"An error occurred: {str(e)}", 500



    def ping(self):
        """
        Endpoint simple de verificación de estado que responde con 'pong'.

        Returns:
            str: La cadena "pong".
        """ 
        return "pong"


## def main ()
if __name__ == '__main__':
    """
    Punto de entrada principal para la aplicación del servidor.

    Este script se puede ejecutar con o sin argumentos de línea de comandos. Si no se proporcionan argumentos,
    inicializa y ejecuta el servidor con configuraciones predeterminadas. Si se proporcionan exactamente siete argumentos,
    inicializa y ejecuta el servidor con las configuraciones especificadas.

    Argumentos de línea de comandos:
        1. language (str): La configuración de idioma para el sistema.
        2. stt (str): El servicio de reconocimiento de voz a texto a utilizar.
        3. whisperSize (str): El tamaño del modelo Whisper a utilizar para STT.
        4. llm (str): El modelo de lenguaje grande a utilizar.
        5. localModels (str): Los modelos locales a utilizar.
        6. tts (str): El servicio de texto a voz a utilizar.
        7. port (int): El puerto en el que se ejecutará el servidor Flask.

    Raises:
        ValueError: Si el argumento del puerto proporcionado no es un entero válido.
        SystemExit: Si el número de argumentos es inválido o si el argumento del puerto es inválido.
    """
    arguments_number  = len(sys.argv) - 1
    if(arguments_number == 0): #When args not given
        servidor = Servidor()
        servidor.run()
    elif(arguments_number == 7): #Args given
        servidor = Servidor(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
        try:
            port = int(sys.argv[7])  
            servidor.run(debug=False, port= port)
        except ValueError:  # Manejar el error si la conversión falla
            print("Bad Port.")
            exit (-1)
        
    else:
        print("Invalid arguments number") 
        exit (-1)
    
