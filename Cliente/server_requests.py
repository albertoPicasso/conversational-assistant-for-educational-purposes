import requests 

class Server_requests:
    def __init__(self, serverurl, session):
        self.SERVER_URL = serverurl
        self.session = session




    def register_user(self):
        '''
        Attempts to connect to the server 3 times, if unsuccessful, it returns False.
        '''
        flag = False
        counter = 0

        while (counter < 3):
            try:
                response = self.session.get(self.SERVER_URL)
                if response.status_code == 200:
                    print("Register Success:")
                    print(response.text)
                    return True
                elif response.status_code == 500:
                        print('Unable to register')
                        print(response.text)
                        print('Retrying to establish connection: {}/2'.format(counter))
                        counter += 1 
            except requests.exceptions.ConnectionError:
                print("Unable to connect.")
                print('Retrying to establish connection: {}/2'.format(counter))
                counter += 1 

        #Change by an exception
        return False



    def send_wav(self, filename: str):
        url_servidor = self.SERVER_URL + "/upload_wav"
        audioname = "outputClient.wav"
        try:
            with open(filename, 'rb') as archivo:
                file = {'wav_file': (filename, archivo, 'audio/wav')}
                response = self.session.post(url_servidor, files=file)
                
                if response.status_code == 200:
                    print('Success')
                    #Save received audio
                    with open(audioname, 'wb') as archivo_local:
                        archivo_local.write(response.content)
                        return audioname
                elif response.status_code == 401:
                    print('User should be registered')
                elif response.status_code == 404:
                    print('No audio wav received or selected')
                elif response.status_code == 500:
                    print('Internal server error')
                    print(response.text)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return "fail"


    def logout(self):
        global session
        url_servidor = self.SERVER_URL + "/logout"
        try:
            #Logouts request
            response = self.session.get(url_servidor)
            
            # Check return code
            if response.status_code == 200:
                return "Logout exitoso. Código de estado: 200"
            else:
                return f"Error en el logout. Código de estado: {response.status_code}"
        except requests.RequestException as e:
            return f"Error al realizar la petición: {e}"