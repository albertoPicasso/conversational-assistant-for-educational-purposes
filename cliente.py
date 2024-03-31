import requests

# URL del servidor Flask
SERVER_URL = 'http://localhost:5000'

# Crear un objeto de sesión para mantener la sesión entre solicitudes
session = requests.Session()

def make_request():
    global session
    # Mensaje a enviar
    mensaje = 'Hola, este es un mensaje enviado desde el cliente Python.'

    # Crear el cuerpo de la solicitud POST con el mensaje
    payload = {'mensaje': mensaje}  
    
    # Realizar una solicitud POST al servidor
    response = session.post(SERVER_URL, data=payload)

    # Imprimir la respuesta del servidor
    print("Respuesta del servidor:")
    print(response.text)

def enviar_mp3():
    global session
    url_servidor = SERVER_URL + "/subir_mp3"

    with open('archivo.mp3', 'rb') as archivo:
        archivos = {'mp3_file': ('archivo.mp3', archivo, 'audio/mp3')}
        respuesta = session.post(url_servidor, files=archivos)

    print(respuesta.text)
    
if __name__ == '__main__':
    # Realizar dos solicitudes al servidor Flask
    enviar_mp3()
    enviar_mp3()
