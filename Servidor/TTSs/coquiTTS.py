from .ttsInterface import TtsInterface
import torch
from TTS.api import TTS
import os 
import wave

## Implementación de CoquiTTS para Texto a Voz (TTS)

class CoquiTTS(TtsInterface):
    """
    Esta clase implementa la interfaz TtsInterface para la funcionalidad de Texto a Voz (TTS)
    utilizando la biblioteca Coqui TTS.

    Toma el nombre de un modelo TTS como argumento en el constructor y utiliza
    la API de Coqui TTS para convertir texto a voz y guardar el audio generado en un archivo.
    """

    def __init__(self, model):
        """
        Inicializa el objeto CoquiTTS.

        Args:
            model (str): El nombre del modelo Coqui TTS a utilizar (por ejemplo, "tts_models/en/ljspeech").
        """
        # Configura automáticamente el dispositivo (CPU o GPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Cargar el modelo Coqui TTS en el dispositivo elegido
        self.model = model
        self.TTS = TTS(model_name=self.model).to(self.device)

    def speak(self, text: str, uid: str) -> str:
        """
        Convierte texto a voz utilizando el modelo Coqui TTS y guarda el audio en un archivo.

        Args:
            text (str): El texto a convertir en voz.
            uid (str): El identificador de usuario para crear una ruta única para el archivo de audio.

        Returns:
            str: El nombre del archivo de audio generado en formato wav.
        """
        # Si la solicitud falla, lanzará una excepción que será capturada en la función superior
        # Definir el nombre del archivo de salida
        nombre = "output.wav"  
        ruta = os.path.join(os.getcwd(), "tempUserData", uid, nombre)
        

        ##Se divide la respuesta en una cantidad de palabras que la memoria del ordenador sea capaz de manejar
        chunk_length = 150

        # Split the text into words
        words = text.split()

        # Initialize the list of chunks
        chunks = []

        # Iterate over the words
        for i in range(0, len(words), chunk_length):
            # Get a chunk of words
            chunk_words = words[i:i + chunk_length]

            # Join the words into a string
            chunk_text = ' '.join(chunk_words)

            # Add the chunk to the list
            chunks.append(chunk_text)

        
        if os.path.exists(ruta):
            os.remove(ruta)
        
        i= 0
        namelist = []
        for chunk in chunks:
            #Calcular Ruta temporal
            nombrealt = "output"+str(i)+".wav"
            rutaAlt = os.path.join(os.getcwd(), "tempUserData", uid, nombrealt)
            namelist.append(rutaAlt)
            # Realizar la síntesis de texto a voz y guardar el audio
            self.TTS.tts_to_file(text=chunk, file_path=rutaAlt, speed=1.2, split_sentences=False)
            i = i+1
        

        data= []
        for name in namelist:
            w = wave.open(name, 'rb')
            data.append( [w.getparams(), w.readframes(w.getnframes())] )
            os.remove(name)
            w.close()
            
        output = wave.open(ruta, 'wb')
        output.setparams(data[0][0])
        for i in range(len(data)):
            output.writeframes(data[i][1])
        output.close()

        
        

        # Devolver el nombre del archivo de audio generado
        return ruta
