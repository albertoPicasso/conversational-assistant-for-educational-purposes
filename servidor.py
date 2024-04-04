from flask import Flask, session, request, send_file
import uuid
from codigos.STTFolder.localWhisper import LocalWhisper
from codigos.STTFolder.remoteWhisper import RemoteWhisper
from codigos.LLMFolder.openAIAPI import OpenAIAPI
from codigos.TTSFolder.coquiTTS import CoquiTTS
from codigos.TTSFolder.openAITTS import OpenAITTS
import os
from openai import OpenAI

class Servidor:
    def __init__(self):
        ##Server configs
        self.app = Flask(__name__)
        self.app.secret_key = 'tu_clave_secreta'
        ## Adding rules
        self.app.add_url_rule('/', 'register_user', self.register_user, methods=['GET'])
        self.app.add_url_rule('/upload_wav', 'upload_wav', self.upload_wav, methods=['POST'])
        self.app.add_url_rule('/ping', 'ping', self.ping, methods=['GET'])
        self.app.add_url_rule('/logout', 'logout', self.logout, methods=['GET'])
        ## Server variables
        self.systemMessage = "asistente tan simpatico "#"You are an Spanish teacher doing a speaking test. You must to act like a teacher, dont say that you are chatgpt. Do questions one by one and wait to my anwser. You should do 3 questions. At the end you send me a message whith a score using MCER levels and finally why i have this level and how to improve it . Remember that you only have 3 questions so choose wisely, dont do silly questions.I need that you more accurate whit scores. Not everyone can be a B2. Look the tenses, the complexiti of the phrases. Please be more accurate Speak every time in spanish."

        ##Interface Configs
#--------------------REMOTE------------------------------------------·#
        self.client = OpenAI(api_key=os.getenv("OPENAIKEY"), base_url="https://api.openai.com/v1")
        ##STT        
        #self.STT = RemoteWhisper("whisper-1", self.client)

        ##LLM
        self.model = "gpt-3.5-turbo-0125"
        self.LLM = OpenAIAPI(self.client, self.model)

        #TTS
        #self.TTS = OpenAITTS("onyx")

#--------------------LOCAL------------------------------------------·#
        ##STT
        self.modelSize = "small"
        self.STT = LocalWhisper(self.modelSize)
        
        ##LLM
        #self.client = OpenAI(base_url="http://192.168.1.135:1234/v1", api_key="lm-studio") 
        #self.model = "local-model"

        #TTS
        self.TTS = CoquiTTS("tts_models/es/css10/vits")


    def register_user(self):
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
            state = self.addMessageToChat(self.systemMessage, "system", state)

            # Save state in session
            session['estado'] = state
            
            self.createUserDirectory(user_id)

            return 'User {} registered successfully.'.format(user_id), 200

        except Exception as e:
            # Manejo de excepciones genérico
            return 'Error registering user: {}'.format(str(e)), 500

  
    def upload_wav(self):
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
            path = os.path.join(os.getcwd(), user_id, filename)
            wav.save(path)

            # Transcribe the WAV file
            text = self.STT.transcribe(path)

            # Get session state
            state = session.get('estado', {})

            # Add user message to chat
            state = self.addMessageToChat(text, "user", state)

            # Ask to language model
            messages_list = state['mensajes']
            response = self.LLM.request_to_llm(messages_list)

            # Add assistant response to chat
            state = self.addMessageToChat(response, "assistant", state)

            # Generate audio WAV
            outname = self.TTS.speak(response, user_id)
            #self.printAllChat(state)

            # Update session state
            session['estado'] = state

            # Return the audio file
            return send_file(outname, mimetype="application/octet-stream")

        except Exception as e:
            # Handle unexpected errors
            return f"An error occurred: {str(e)}", 500
      
    
    def logout(self):
       
        try:
            if 'user_id' in session:
                user_id = session['user_id']
                session.pop('user_id')
            
            # Remove client directory 
            os.system(f'rm -rf {user_id}')
            print(f"Carpeta {user_id} y su contenido han sido eliminados exitosamente.")
            return 'Logout successfully.', 200
                
        except Exception as e:
            print(f"Error al intentar borrar la carpeta {user_id}: {e}")
            return f"An error occurred: {str(e)}", 500


        
    def run(self, debug=False):
        self.app.run(debug=debug,host='0.0.0.0', port=5000)


    ## # Add new messages to session['mensajes'] whit format [role,message]
    def addMessageToChat(self, message, role, state):
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
        lista_mensajes = state['mensajes']
        print('Lista de mensajes ')
        for mensaje in lista_mensajes:
            print(mensaje)

    def ping(self): 
        return "pong"
    
    def createUserDirectory(self, name):
    
        #Path to new directory / folder
        path_to_directory = os.path.join(os.getcwd(), name)

        #Create directory
        os.mkdir(path_to_directory)
        print(f"The directory'{name}' has been created successfully")
        

if __name__ == '__main__':
    servidor = Servidor()
    servidor.run(debug=True)
