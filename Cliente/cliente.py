from pynput import keyboard 
import threading
import queue
import os 
import pyaudio
import wave
import requests


#server = Servidor()

# URL del servidor Flask
SERVER_URL = 'http://192.168.0.16:5000'

# Crear un objeto de sesión para mantener la sesión entre solicitudes
session = requests.Session()


#Set audio parameters 
FORMAT = pyaudio.paInt16    # Audio Data format (16 bits)
CHANNELS = 1                # NChannel numbers
RATE = 44100                # Sampling rate Hz
CHUNK = 1024                # chunk size


#Recording flag
recording = False

#Open the stream
stream =None

#PyAudio object
p = pyaudio.PyAudio()

# list for store audio data
frames = []

#Audio name
filename = "input.wav"

#Queue for threads communication
q = queue.Queue()

#Semaphore to stop the transcribing method til saving audio
sem = threading.Semaphore(0)

#Semaphore to stop chat til speaking text audio
sem2 = threading.Semaphore(0)



def on_press(key):
    global recording
    global stream
    if key == keyboard.Key.space and not recording:
        try:
            recording = True
            openStream()
            #Create the recording thread 
            ##FORK
            recording_thread = threading.Thread(target=audioRecord)     ##Execute the audioRecord method
            recording_thread.start()
        except Exception as e:
            print(f"Ocurrió un error al iniciar la grabación: {e}")
    
    if key == keyboard.KeyCode.from_char('s'): 
        try:
            logout()
            listener.stop()
            p.terminate
            exit(0)   
        except Exception as e:
            print(f"Ocurrió un error saliendo : {e}") 
        


def on_release(key):
    global recording 
    global filename
    global sem2
    if key == keyboard.Key.space and recording:
        try:
            q.put(True)
            # Wait to stop saving audio
            sem.acquire()
            #name = server.launch(filename)
            name = send_wav()
            if (name == 'fail'):
                print("Error en la recepcion del audio")
                exit (-1)
            playAudio(name)
            recording = False
            sem2.release()
        except Exception as e:
            print(f"Ocurrió un error soltando la tecla: {e}")
            pass





def register_user():
    '''
    Attempts to connect to the server 3 times, if unsuccessful, it returns False.
    '''
    global session
    flag = False
    counter = 0

    while (counter < 3):
        try:
            response = session.get(SERVER_URL)
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

    return False

def send_wav():
    global session
    url_servidor = SERVER_URL + "/upload_wav"
    audioname = "outputClient.wav"
    try:
        with open(filename, 'rb') as archivo:
            file = {'wav_file': (filename, archivo, 'audio/mp3')}
            response = session.post(url_servidor, files=file)
            
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
    

def logout():
    global session
    url_servidor = SERVER_URL + "/logout"
    try:
        # Realiza la petición para hacer logout
        response = session.get(url_servidor)
        
        # Verifica el código de estado de la respuesta
        if response.status_code == 200:
            return "Logout exitoso. Código de estado: 200"
        else:
            return f"Error en el logout. Código de estado: {response.status_code}"
    except requests.RequestException as e:
        return f"Error al realizar la petición: {e}"

##AUDIO
def audioRecord(): 
    global recording
    global frames 
    global stream
    global sem
    while (recording):                                       
        data = stream.read(CHUNK)
        frames.append(data)

        try:
            #Check events in queue
            if q.get_nowait():
                wf = wave.open(filename, 'wb')  # W for overwrite the actual .wav
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                closeStream()
                #Clean Frames list
                frames = []
                #Release the semaphore
                sem.release()
                break
        except queue.Empty:
            pass
    
def openStream(): 
    global stream
    try:
        stream = p.open(format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK)
    except Exception as e:
            print(f"Ocurrió un error abriendo el stream: {e}")

def closeStream():
    global stream
    stream.stop_stream()
    stream.close()

def playAudio(audio): 
    global sem2
    with wave.open(audio, 'rb') as wav_file:
        # Configurar PyAudio
        
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wav_file.getsampwidth()),
                            channels=wav_file.getnchannels(),
                            rate=wav_file.getframerate(),
                            output=True)


        # Leer y reproducir los datos del archivo WAV
        data = wav_file.readframes(1024)
        while data:
            stream.write(data)
            data = wav_file.readframes(1024)

        # Detener la reproducción
        stream.stop_stream()
        stream.close()
        p.terminate()
        sem2.release()






def clear_screen():
    if os.name == 'posix':  # Para sistemas Unix/Linux
        os.system('clear')
    elif os.name == 'nt':  # Para Windows
        os.system('cls')
    else:
        # Sistema operativo no compatible
        pass 

# Set the listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    clear_screen()

    registerSuccess = register_user()    
    if registerSuccess is False: 
        exit (-1)
        
    print("Listo!")
    listener.join() 
 