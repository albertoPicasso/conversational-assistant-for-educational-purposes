import requests 
import base64

class Server_requests:
    def __init__(self, serverurl, session):
        self.SERVER_URL = serverurl
        self.session = session




    def register_user(self):
        '''
        Attempts to connect to the server 3 times, if unsuccessful, it returns False.
        '''
        counter = 0

        while (counter < 3):
            try:
                response = self.session.get(self.SERVER_URL)
                if response.status_code == 200:
                    print("Register Success:")
                    print(response.text)
                    return 
                elif response.status_code == 500:
                        print('Unable to register')
                        print(response.text)
                        print('Retrying to establish connection: {}/2'.format(counter))
                        counter += 1 
            except requests.exceptions.ConnectionError:
                print("Unable to connect.")
                print('Retrying to establish connection: {}/2'.format(counter))
                counter += 1 

        raise ConnectionError ("Cannot connect to server ")



    def send_wav(self, filename: str):
        url_servidor = self.SERVER_URL + "/upload_wav"
        audioname = "outputClient.wav"
        
        with open(filename, 'rb') as archivo:
            file = {'wav_file': (filename, archivo, 'audio/wav')}
            response = self.session.post(url_servidor, files=file)                
            if response.status_code == 200:
                #Recieve and process data
                json_data = response.json()
                audio_base64 = json_data['audio']
                audio_data = base64.b64decode(audio_base64)
                flag_value = json_data['flag']

                with open(audioname, 'wb') as archivo_local:
                    archivo_local.write(audio_data)
                    return [audioname, flag_value]
                
            elif response.status_code == 401:
                print('User should be registered')
            elif response.status_code == 404:
                print('No audio wav received or selected')
            elif response.status_code == 500:
                print('Internal server error')
                print(response.text)
      


    def logout(self):
        
        url_servidor = self.SERVER_URL + "/logout"
        #Logouts request
        response = self.session.get(url_servidor)
            
        # Check return code
        if response.status_code != 200:
            raise TypeError ("Unable to logout")
        