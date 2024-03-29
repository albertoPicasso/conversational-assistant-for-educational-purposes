from flask import Flask, session, request
import uuid

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener el mensaje enviado por el cliente
        mensaje = request.form['mensaje']

        # Obtener o generar un identificador de sesión para el cliente
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())  # Genera un UUID único

        # Obtener el identificador de sesión del cliente
        user_id = session['user_id']

        # Verificar si el cliente tiene un estado almacenado en la sesión
        if 'estado' not in session:
            # Si no tiene, inicializar un estado vacío para ese cliente
            session['estado'] = {}

        # Obtener el estado del cliente desde la sesión
        estado = session['estado']

        # Almacenar el mensaje en la lista de mensajes del cliente
        if 'mensajes' not in estado:
            estado['mensajes'] = []  # Inicializar la lista si no existe
        estado['mensajes'].append(mensaje)

        # Guardar el estado actualizado en la sesión
        session['estado'] = estado
        lista_mensajes = estado['mensajes']
        print('Lista de mensajes del cliente (ID {}):'.format(user_id))
        for mensaje in lista_mensajes:
            print(mensaje)
        
        return 'Mensaje almacenado correctamente.'

    elif request.method == 'GET':
        # Obtener o generar un identificador de sesión para el cliente
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())  # Genera un UUID único

        # Obtener el identificador de sesión del cliente
        user_id = session['user_id']

        # Verificar si el cliente tiene un estado almacenado en la sesión
        if 'estado' not in session:
            # Si no tiene, inicializar un estado vacío para ese cliente
            session['estado'] = {}

        # Obtener el estado del cliente desde la sesión
        estado = session['estado']

        # Obtener la lista de mensajes del cliente
        mensajes = estado.get('mensajes', [])

        return 'ID de usuario: {}. Mensajes del cliente: {}'.format(user_id, mensajes)

if __name__ == '__main__':
    app.run(debug=True)
