import requests

# URL del servidor Flask
SERVER_URL = 'http://localhost:5000'
session = requests.Session()


def make_request():
    global session
    # Crear un objeto de sesión
    
    # Realizar una solicitud GET al servidor
    response = session.get(SERVER_URL)

    # Imprimir la respuesta del servidor
    print("Respuesta del servidor:")
    print(response.text)

 
    # Realizar una nueva solicitud GET al servidor para verificar que mantiene la sesión
    response = session.get(SERVER_URL)

    # Imprimir la respuesta del servidor
    print("\nRespuesta del servidor (segunda solicitud):")
    print(response.text)

     # Realizar una nueva solicitud GET al servidor para verificar que mantiene la sesión
    response = session.get(SERVER_URL)

    # Imprimir la respuesta del servidor
    print("\nRespuesta del servidor (tercera solicitud):")
    print(response.text)

if __name__ == '__main__':
    # Realizar una solicitud al servidor Flask
    make_request()
    make_request()