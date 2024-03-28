from flask import Flask, session, request
import uuid

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

@app.route('/')
def index():
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

    # Realizar cualquier operación que necesites con el estado del cliente
    # Por ejemplo, incrementar un contador
    estado['contador'] = estado.get('contador', 0) + 1

    # Guardar el estado actualizado en la sesión
    session['estado'] = estado

    return 'ID de usuario: {}. Contador para este cliente: {}'.format(user_id, estado['contador'])

if __name__ == '__main__':
    app.run(debug=True)
