from pynput import keyboard 
import threading
import queue
import os 
import pyaudio
import wave
import requests
from server_requests import Server_requests 
import signal
import sys


# Object needed to request to server
SERVER_URL = 'http://192.168.0.16:5000'
session = requests.Session()
sr = Server_requests(SERVER_URL, session)


#Set audio parameters 
FORMAT = pyaudio.paInt16        # Audio Data format (16 bits)
CHANNELS = 1                    # NChannel numbers
RATE = 44100                    # Sampling rate Hz
CHUNK = 1024                    # chunk size


recording = False               #Recording flag
stream =None
p = pyaudio.PyAudio()
frames = []                     # list for store audio data
filename = "input.wav"


q = queue.Queue()               #Notify stop recording
sem = threading.Semaphore(0)    #Semaphore to stop the transcribing method til saving audio
sem2 = threading.Semaphore(0)   #Semaphore to stop chat til speaking text audio


# Key management
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
            restart_connection()
     
        
def on_release(key):
    global recording 
    global filename
    global sem2
    if key == keyboard.Key.space and recording:
        try:
            q.put(True)
            # Wait to stop saving audio
            sem.acquire()
            data = sr.send_wav(filename)
            name = data[0]
            isEnd = data[1]
            print(isEnd)
            playAudio(name)
            recording = False
            sem2.release()
        except Exception as e:
            print(f"Ocurrió un error soltando la tecla: {e}")
            restart_connection()



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
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

def closeStream():
    global stream
    stream.stop_stream()
    stream.close()

def playAudio(audio): 
    global sem2
    with wave.open(audio, 'rb') as wav_file:
        # Configure PyAudio
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wav_file.getsampwidth()),
                            channels=wav_file.getnchannels(),
                            rate=wav_file.getframerate(),
                            output=True)

        #Read wav file
        data = wav_file.readframes(1024)
        while data:
            stream.write(data)
            data = wav_file.readframes(1024)

        # Stop playing
        stream.stop_stream()
        stream.close()
        p.terminate()
        sem2.release()



#Aux functions
def exit_secuence():
    try:
        print("Exit")
        sr.logout()
        listener.stop()
        p.terminate
        exit (0)
    except Exception as e:
            print(f"Exit error: {e}")
            sys.exit(-1)  
            
def restart_connection(): 
    try:
        print("Restarting connection")
        sr.logout()
        sr.register_user()
    except Exception as e:
            print(f"Restart error: {e}")
            sys.exit(-1)  
    

def graceful_exit(signal, frame):
    print("\nGracefully exiting...")
    exit_secuence()
    
def clear_screen():
    if os.name == 'posix':  # Unix/Linux
        os.system('clear')
    elif os.name == 'nt':  # Windows
        os.system('cls')
    else:
        # Not supported
        pass 

# Set the listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    signal.signal(signal.SIGINT,  graceful_exit)
    clear_screen()
    try:
        sr.register_user()    
    except Exception as e:
            print(f"Ocurrió un error soltando la tecla: {e}")
            exit (-1)
        
    print("Listo!")
    listener.join() 
 