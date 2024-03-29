import requests

# URL del servidor Flask
SERVER_URL = 'http://localhost:5000'
session = requests.Session()


def make_request():
    global session
    # Crear un objeto de sesión
    
    # Mensaje a enviar
    mensaje = 'Hola, este es un mensaje enviado desde el cliente Python.'

    # Crear el cuerpo de la solicitud POST con el mensaje
    payload = {'mensaje': mensaje}  
    
    # Realizar una solicitud GET al servidor
    response = session.post(SERVER_URL, data=payload)

    # Imprimir la respuesta del servidor
    print("Respuesta del servidor:")
    print(response.text)
    
     # Mensaje a enviar
    mensaje = 'Hola, este es el segundo mensaje enviado desde el cliente Python.'

    # Crear el cuerpo de la solicitud POST con el mensaje
    payload = {'mensaje': mensaje}  
    
    # Realizar una solicitud GET al servidor
    response = session.post(SERVER_URL, data=payload)

    # Imprimir la respuesta del servidor
    print("Respuesta del servidor:")
    print(response.text)



if __name__ == '__main__':
    # Realizar una solicitud al servidor Flask
    make_request()
    make_request()