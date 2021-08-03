'''
1º [Linha 5] - Importando a classe Flask do módulo flask
'''

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World'
