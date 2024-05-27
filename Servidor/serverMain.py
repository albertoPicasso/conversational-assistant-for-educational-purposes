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
        Initialize the server configuration and set up routes and database.

        This constructor does the following:
        - Initializes a Flask application.
        - Sets a secret key for the Flask application.
        - Initializes auxiliary functions.
        - Adds URL rules for various endpoints.
        - Creates a folder for temporary user data if it doesn't exist.
        - Creates a database for user data if it doesn't exist, and adds a default user.

        Attributes:
            app (Flask): The Flask application instance.
            aux (Aux_functions): An instance of auxiliary functions for various utility operations.

        Raises:
            sqlite3.Error: If there is an error adding the default user to the database.
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
        Run the Flask server with the specified configurations.

        This method sets up logging, initializes various components of the system (such as STT, LLM, and TTS),
        and starts the Flask server.

        Args:
            language (str, optional): The language setting for the system. Default is "es".
            stt (str, optional): The speech-to-text service to be used. Default is "local".
            whisperSize (str, optional): The size of the Whisper model to be used for STT. Default is "small".
            llm (str, optional): The large language model to be used. Default is "remoto".
            localModels (str, optional): The local models to be used. Default is "Gemma".
            tts (str, optional): The text-to-speech service to be used. Default is "local".
            port (int, optional): The port on which the Flask server will run. Default is 5000.

        Raises:
            Exception: If an unhandled exception occurs during the initialization of system components.
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
        Register a new user based on the JSON data received in the request.

        This method extracts user information from a JSON payload, attempts to add the user
        to the database, and handles any potential errors during the process. It also logs 
        the success or failure of the registration attempt.

        Returns:
            tuple: A tuple containing a message and an HTTP status code.
                - "ok", 200: If the user is successfully registered.
                - "User already exist", 409: If there is an attempt to register an existing user.
                - "Something gone wrong", 500: If an unhandled exception occurs.
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
        Authenticate a user based on the JSON data received in the request.

        This method extracts the username and password from a JSON payload, verifies the user's credentials,
        and handles the login process. It also logs the success or failure of the login attempt.

        Returns:
            tuple: A tuple containing a message and an HTTP status code.
                - "Verifing user: OK", 200: If the user is successfully authenticated.
                - "Verifing user: NOT OK", 401: If the authentication fails.
                - "something failed", 500: If the request format is incorrect or an unhandled exception occurs.
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
        Register a new user session and initialize the session state.

        This method assigns a unique user ID to the session if it doesn't already have one,
        initializes the session state and messages, adds a system message to the chat,
        creates a user directory, and logs the registration success or failure.

        Returns:
            tuple: A tuple containing a message and an HTTP status code.
                - 'User {user_id} registered successfully.', 200: If the user session is successfully registered.
                - 'Error registering user: {error_message}', 500: If an unhandled exception occurs during registration.
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
        Handle the upload of a WAV file, transcribe its contents, interact with the language model,
        and return a synthesized response.

        This method performs the following actions:
        - Checks if the user is authenticated.
        - Validates the presence and selection of a WAV file in the request.
        - Saves the uploaded WAV file to a temporary directory.
        - Transcribes the WAV file to text using the STT system.
        - Adds the transcribed text to the chat history.
        - Sends the chat history to a language model and receives a response.
        - Checks if the conversation has ended and prepares an evaluation message if necessary.
        - Adds the assistant's response to the chat history.
        - Converts the response to speech using the TTS system.
        - Encodes the audio response in base64 and returns it along with an end-of-conversation flag.

        Returns:
            Response: A JSON response containing the encoded audio and end-of-conversation flag, or an error message and status code.
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
        Log out the user by removing the user ID from the session and deleting the user's temporary data directory.

        This method performs the following actions:
        - Checks if the user is authenticated.
        - Removes the user ID from the session.
        - Deletes the user's temporary data directory.
        - Logs the successful logout.

        Returns:
            tuple: A tuple containing a message and an HTTP status code.
                - 'Logout successfully.', 200: If the user is successfully logged out.
                - 'An error occurred: {error_message}', 500: If an unhandled exception occurs during the logout process.
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
        Delete a user based on the JSON data received in the request.

        This method extracts the username and password from a JSON payload, attempts to delete the user
        from the database, and handles any potential errors during the process. It also logs the success
        or failure of the deletion attempt.

        Returns:
            tuple: A tuple containing a message and an HTTP status code.
                - "User deleted", 200: If the user is successfully deleted.
                - "User not found", 400: If the user is not found or the deletion fails.
                - "An error occurred: {error_message}", 500: If an unhandled exception occurs.
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
        Simple health check endpoint that responds with 'pong'.

        Returns:
            str: The string "pong".
        """ 
        return "pong"


## def main ()
if __name__ == '__main__':
    """
    Main entry point for the server application.

    This script can be run with or without command-line arguments. If no arguments are provided,
    it initializes and runs the server with default settings. If exactly seven arguments are provided,
    it initializes and runs the server with the specified settings.

    Command-line Arguments:
        1. language (str): The language setting for the system.
        2. stt (str): The speech-to-text service to be used.
        3. whisperSize (str): The size of the Whisper model to be used for STT.
        4. llm (str): The large language model to be used.
        5. localModels (str): The local models to be used.
        6. tts (str): The text-to-speech service to be used.
        7. port (int): The port on which the Flask server will run.

    Raises:
        ValueError: If the provided port argument is not a valid integer.
        SystemExit: If the number of arguments is invalid or if the port argument is invalid.
    """
    arguments_number  = len(sys.argv) - 1
    if(arguments_number == 0): #When args not given
        servidor = Servidor()
        servidor.run(debug=False)
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
    
