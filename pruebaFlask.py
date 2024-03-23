from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '¡Hola, mundo! Este es mi primer servidor Flask.'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
