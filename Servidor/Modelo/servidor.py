from flask import Flask, session, request, send_file, jsonify
import uuid
import os
from openai import OpenAI
import logging
import base64
import sys

from Modelo.aux_functions import Aux_functions


class Servidor:
    def __init__(self):

        
        ##Server configs
        self.app = Flask(__name__)
        self.app.secret_key = 'tu_clave_secreta'
        self.aux = Aux_functions()
      
        ## Adding rules
        self.app.add_url_rule('/', 'register_user', self.register_user, methods=['GET'])
        self.app.add_url_rule('/upload_wav', 'upload_wav', self.upload_wav, methods=['POST'])
        self.app.add_url_rule('/ping', 'ping', self.ping, methods=['GET'])
        self.app.add_url_rule('/logout', 'logout', self.logout, methods=['GET'])
        ## Server variables
        #self.systemMessage = "You are an Spanish teacher doing a speaking test. You must to act like a teacher, dont say that you are chatgpt. Do questions one by one and wait to my anwser. You should do 1 question. At the end you send me a message whith a score using MCER levels and finally why i have this level and how to improve it . Remember that you only have 3 questions so choose wisely, dont do silly questions.I need that you more accurate whit scores. Not everyone can be a B2. Look the tenses, the complexiti of the phrases. Please be more accurate Speak every time in spanish. Ademas necesito que transcribas lo numeros, por ejemplo si hay un 12 quiero que pongas doce , o si pone B1 pongas be uno si pone a2 que pongas a dos, El mensaje en el que vaya la puntuacion evaluacion final quiero que empiece por [END]"
        



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
       
        try:
            if 'user_id' in session:
                user_id = session['user_id']
                session.pop('user_id')
            # Remove client directory 
            os.system(f'rm -rf {user_id}')
            self.app.logger.info (f'- Logout user Succsessfully - id {user_id} /  ')
            return 'Logout successfully.', 200
                
        except Exception as e:
            self.app.logger.error('Unhandled exception occurred', exc_info=e)
            return f"An error occurred: {str(e)}", 500

    


    def ping(self): 
        return "pong"
    

        
    def run(self, language = "es", stt = "local", whisperSize = "small" , llm = "remoto", localModels = "Gemma", tts = "local", port = 5000):
        
        #Set logger
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(formatter)
        self.app.logger.addHandler(file_handler)
        self.app.logger.setLevel(logging.DEBUG)
        self.app.logger.critical(f'Server Start ')

        #Set Interfaces
        print("Language:", language)
        print("STT:", stt)
        print("WhisperSize:", whisperSize)
        print("LLM:", llm)
        print("TTS:", tts)
        
        print("Local Models:", localModels)
        print("Port:", port)
        
        
        self.lang = language
        
        ##Interface Config
        try:
            self.systemMessage = Aux_functions.selectSysMessage(language)
            self.STT = Aux_functions.createSTT(stt, whisperSize)
            self.LLM = Aux_functions.createLLM(llm)
            self.TTS = Aux_functions.createTTS(tts,language)
            self.teacherMode = Aux_functions.createLenguageTeacher(self.lang)
        except Exception as e:
            self.app.logger.error('Unhandled exception occurred. Leaving...', exc_info=e)
            sys.exit(-1)
       
        self.app.run(debug=True,host='0.0.0.0', port=port,  use_reloader=False)
       

    def serverHelloWorld(self): 
        print("Hello word")

## def main ()
if __name__ == '__main__':
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
    
    #servidor = Servidor()
    #servidor.run(debug=False)
