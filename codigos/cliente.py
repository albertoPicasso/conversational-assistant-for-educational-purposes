from servidor import Servidor
from pynput import keyboard 
import threading
import queue
import os 
import pyaudio
import wave
import requests


server = Servidor()

# URL del servidor Flask
SERVER_URL = 'http://localhost:5000'

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
filename = "Entrada.wav"

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
            name = server.launch(filename)
            playAudio(name)
            #send_wav()
            recording = False
            sem2.release()
        except Exception as e:
            print(f"Ocurrió un error soltando la tecla: {e}")

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



def send_wav():
    global session
    url_servidor = SERVER_URL + "/subir_mp3"

    with open(filename, 'rb') as archivo:
        archivos = {'mp3_file': (filename, archivo, 'audio/mp3')}
        respuesta = session.post(url_servidor, files=archivos)

    print(respuesta.text)
    

def register_user():
    global session
    # Realizar una solicitud POST al servidor
    response = session.get(SERVER_URL)

    # Imprimir la respuesta del servidor
    print("Respuesta del servidor:")
    print(response.text)

# Set the listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    os.system("clear")
    #register_user()
    print("Listo!")
    listener.join() 
 